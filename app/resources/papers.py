from flask_restful import Resource, reqparse
from flask import g

from app.models.papers import PaperModel, QuestionModel
from libs import non_empty_string, date_string
from app import auth, db


class PaperListView(Resource):
    @auth.login_required
    def get(self):
        """返回登陆的老师的所有的试卷的简单信息"""
        papers = PaperModel.query.all()
        data = [paper.to_show() for paper in papers]
        return {"status": "ok", "data": data}

    @auth.login_required
    def post(self):
        """增加一张试卷"""
        parser = reqparse.RequestParser()
        parser.add_argument("paper_name", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("exam_date", required=True, nullable=False, type=date_string)
        parser.add_argument("sum_score", required=True, nullable=False, type=int)
        parser.add_argument("info", required=True)
        parser.add_argument("questions", required=True, nullable=False, type=int, action="append")
        args = parser.parse_args()
        if PaperModel.query.filter_by(name=args["paper_name"]).first():
            return {"status": "failed", "status": "试卷已经存在"}
        if sum(args["questions"]) != args["sum_score"]:
            return {"status": "failed", "message": "各题目总分必须与总分相等"}

        paper = PaperModel(name=args["paper_name"], exam_date=args["exam_date"], sum_score=args["sum_score"],
                           info=args["info"], teacher_id=g.user.id)
        db.session.add(paper)
        db.session.commit()
        for question_num, score in enumerate(args["questions"]):
            question = QuestionModel(question_num=question_num, score_in_paper=score, info=paper.name,
                                     paper_id=paper.id)
            db.session.add(question)
        db.session.commit()
        return {"status": "ok", "message": "添加成功"}

    @auth.login_required
    def delete(self, paper_id):
        """删除一张试卷以及它所包含的所有的小题（如果已经有成绩的话则无法删除）"""
        paper = PaperModel.query.get(paper_id)
        if not paper:
            return {"status": "failed", "message": "此试卷不存在"}
        questions = paper.get_all_question()
        for question in questions:
            db.session.delete(question)
        db.session.commit()
        db.session.delete(paper)
        db.session.commit()
        return {"status": "ok", "message": "删除成功"}


class PaperView(Resource):
    @auth.login_required
    def get(self, paper_id):
        paper = PaperModel.query.get(paper_id)
        if not paper:
            return {"status": "failed", "message": "此试卷不存在"}
        data = paper.to_show_detail()
        return {"status": "ok", "message": "查询成功", "data": data}
