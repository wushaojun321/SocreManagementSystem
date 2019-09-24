import uuid

from flask_restful import Resource, reqparse, abort
from flask import request, g

from libs import non_empty_string, password_string
from app import auth, db, app
from app.models.others import TokenModel
from app.models.teacher import TeacherModel


@auth.verify_token
def verify_token(token):
    if TokenModel.get_user_by_token(token):
        return True
    return False


@app.before_request
def load_user():
    value = request.headers.get("Authorization")
    if not value:
        g.user = None
        return
    value = value.replace("Bearer ", "")
    teacher = TokenModel.get_user_by_token(value=value)
    if not teacher:
        g.user = None
        return
    g.user = teacher


class TokenView(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("password", required=True, nullable=False, type=password_string)

        args = parser.parse_args()
        teachers = TeacherModel.query.filter_by(username=args["username"])
        if teachers.count() != 1:
            abort(404, message="can't find this user", status="failed")
        teacher = teachers.first()
        if args["password"] != teacher.password:
            abort(403, message="password is not correct!", status="failed")
        token = TokenModel.query.filter_by(teacher_id=teacher.id, is_delete=False).first()
        if token:
            value = token.value
        else:
            value = str(uuid.uuid4())
            new_token = TokenModel(teacher_id=teacher.id, value=value, is_delete=False)
            db.session.add(new_token)
            db.session.commit()
        g.user = teacher
        return {"status": "ok", "message": "登陆成功", "data": value}

    @auth.login_required
    def delete(self):
        token = TokenModel.query.filter_by(teacher_id=g.user.id, is_delete=False).first()
        if token:
            token.is_delete = True
            db.session.add(token)
            db.session.commit()
        return {"status": "ok", "message": "登出成功"}
