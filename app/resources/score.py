from flask_restful import Resource, reqparse
from flask import g

from app import auth, db
from app.models.score import ScoreModel
from app.models.student import StudentModel
from app.models.papers import PaperModel, QuestionModel
from libs import non_empty_string


class PaperScoreView(Resource):

    @auth.login_required
    def get(self, paper_id):
        paper = PaperModel.query.get(paper_id)
        if not paper:
            return {"status": "failed", "message": "没有这张试卷"}
        data = ScoreModel.get_score_detail(paper)
        return {"status": "ok", "data": data}

    @auth.login_required
    def post(self):
        """增加一张试卷"""
        parser = reqparse.RequestParser()
        parser.add_argument("paper_id", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("student_id", required=True, nullable=False, type=non_empty_string)
        parser.add_argument("scores", required=True, nullable=False, type=int, action="append")
        args = parser.parse_args()
        scores = args["scores"]
        paper_id = args["paper_id"]
        student_id = args["student_id"]
        paper = PaperModel.query.get(paper_id)
        if not paper:
            return {"status": "failed", "message": "找不到这个试卷"}

        student = StudentModel.query.filter_by(student_id=student_id).first()
        if not student:
            return {"status": "failed", "message": "找不到这个学生"}

        questions = QuestionModel.query.filter_by(paper_id=paper_id).order_by(QuestionModel.question_num)

        if questions.count() != len(scores):
            return {"status": "failed", "message": "题目个数不符：此试卷有%s道题目" % questions.count()}
        for question, score in zip(questions, scores):
            if score > question.score_in_paper:
                return {"status": "failed", "message": "第%s道题的分值为%s分,您传入的为%s分" %
                                                    (question.question_num, question.score_in_paper, score)}

        for question, score in zip(questions, scores):
            exist_score = ScoreModel.query.filter_by(question_id=question.id,
                                                     paper_id=paper_id, student_id=student.id).first()
            if exist_score:
                exist_score.points = score
                db.session.add(exist_score)
            else:
                new_score = ScoreModel(question_id=question.id, paper_id=paper_id, student_id=student.id, points=score)
                db.session.add(new_score)
        db.session.commit()
        return {"status": "ok", "message": "添加成功"}
