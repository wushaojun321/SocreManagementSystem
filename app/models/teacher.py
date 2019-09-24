import datetime

from app import db


class TeacherModel(db.Model):

    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(20))

    token = db.Column(db.String(80), nullable=True)
    reg_time = db.Column(db.DateTime, default=datetime.datetime.now)
    last_login_time = db.Column(db.DateTime)
    paper = db.relationship('PaperModel', backref='teacher', lazy='dynamic')
    token = db.relationship('TokenModel', backref='teacher', lazy='dynamic')

    def to_show(self):
        res = dict()
        res["teacher_id"] = self.id
        res["name"] = self.name
        res["username"] = self.username
        return res
