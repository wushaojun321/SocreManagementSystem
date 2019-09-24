from flask import g
from flask_restful import Resource, abort, reqparse


from app import db, auth
from app.models.teacher import TeacherModel
from app.models.others import TokenModel
from libs import non_empty_string, password_string


class TeacherListView(Resource):
    @auth.login_required
    def get(self):
        if g.user.username != "admin":
            abort(403, message="没有权限", status="failed")
        teachers = TeacherModel.query.all()
        res = [t.to_show() for t in teachers]
        return {"status": "ok", "data": res}

    @auth.login_required
    def post(self):
        if g.user.username != "admin":
            abort(403, message="没有权限", status="failed")
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("username", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("password", required=True, nullable=False, type=password_string)

        args = parser.parse_args()
        teachers = TeacherModel.query.filter_by(username=args["username"])
        if teachers.count() > 0:
            abort(403, message="username already exists", status="failed")
        new_teacher = TeacherModel(name=args["name"], username=args["username"],
                                   password=args["password"])

        db.session.add(new_teacher)
        db.session.commit()
        return {"status": "ok", "message": "保存成功"}


class TeacherView(Resource):
    def get(self, teacher_id):
        teacher = TeacherModel.query.get(teacher_id)
        if not teacher:
            abort(404, message="teacher {} doesn't exist".format(teacher_id), status="failed")
        else:
            return teacher.to_show()

    @auth.login_required
    def delete(self, teacher_id):
        if g.user.username != "admin":
            abort(403, message="没有权限", status="failed")
        teacher = TeacherModel.query.get(teacher_id)
        if not teacher:
            abort(404)
        if teacher.username == "admin":
            return {"status": "failed", "message": "不能删除admin"}
        TokenModel.delete_teacher(teacher.id)
        db.session.delete(teacher)
        try:
            db.session.commit()
            g.user = None
            return {"status": "ok", "message": "删除成功"}
        except Exception as e:
            return {"status": "failed", "message": str(e)}


