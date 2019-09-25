from flask_restful import Resource, reqparse

from app.models.student import StudentModel
from app.models.classes import ClassModel
from app import auth, db
from libs import non_empty_string


class StudentListView(Resource):
    @auth.login_required
    def get(self):
        """返回所有的学生"""
        students = StudentModel.query.all()
        data = [student.to_show() for student in students]
        return {"status": "ok", "message": "查询成功", "data": data}

    @auth.login_required
    def post(self):
        """添加一个学生"""
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("student_id", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("student_class_id", required=True, nullable=False, type=int)
        args = parser.parse_args()
        if not ClassModel.query.get(args["student_class_id"]):
            return {"status": "failed", "message": "此班级不存在"}

        if StudentModel.query.filter_by(student_id=args["student_id"]).count() > 0:
            return {"status": "failed", "message": "此学号已经存在"}
        new_student = StudentModel(name=args["name"], student_id=args["student_id"],
                                   student_class_id=args["student_class_id"])
        db.session.add(new_student)
        try:
            db.session.commit()
            return {"status": "ok", "message": "保存成功"}
        except Exception as e:
            db.session.rollback()
            return {"status": "failed", "message": str(e)}


class StudentView(Resource):

    @auth.login_required
    def get(self, _id):
        """返回某一个学生的所有试卷的成绩"""
        pass

    @auth.login_required
    def delete(self, _id):
        student = StudentModel.query.get(_id)
        if not student:
            return {"status": "failed", "message": "学生不存在"}
        db.session.delete(student)
        db.session.commit()
        return {"status": "ok"}
