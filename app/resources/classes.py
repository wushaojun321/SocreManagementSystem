from flask_restful import Resource, abort, reqparse

from app.models.classes import ClassModel
from app import auth, db
from libs import non_empty_string


class ClassListView(Resource):

    @auth.login_required
    def get(self):
        """获取所有班级列表"""
        classes = ClassModel.query.all()
        res = [_class.to_show() for _class in classes]
        return {"status": "ok", "data": res}

    @auth.login_required
    def post(self):
        """新增班级"""
        parser = reqparse.RequestParser()
        parser.add_argument("class_name", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("info")
        args = parser.parse_args()
        _class = ClassModel.query.filter_by(name=args["class_name"]).first()
        if _class:
            abort(403, status="failed", message="此班级已经存在")
        new_class = ClassModel(name=args["class_name"], info=args["info"])
        db.session.add(new_class)
        db.session.commit()
        return {"status": "ok", "message": "添加成功"}


class ClassView(Resource):

    @auth.login_required
    def get(self, class_id):
        """返回班级以及班级的所有学生"""
        _class = ClassModel.query.get(class_id)
        if not _class:
            abort(404, status="failed", message="班级不存在")
        data = _class.to_show_detail()
        return {"status": "ok", "data": data}

    @auth.login_required
    def delete(self, class_id):
        """返回班级以及班级的所有学生"""
        _class = ClassModel.query.get(class_id)
        if not _class:
            abort(404, status="failed", message="班级不存在")
        db.session.delete(_class)
        db.session.commit()
        return {"status": "ok"}