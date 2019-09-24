import datetime

from app import db


class TokenModel(db.Model):

    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(80))
    add_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_delete = db.Column(db.Boolean, default=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

    @classmethod
    def get_user_by_token(cls, value):
        token = cls.query.filter_by(value=value, is_delete=False).first()
        if token:
            return token.teacher

    @classmethod
    def delete_teacher(cls, teacher_id):
        tokens = cls.query.filter_by(teacher_id=teacher_id)
        for token in tokens:
            token.is_delete = True
            db.session.add(token)
        db.session.commit()
