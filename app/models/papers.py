from sqlalchemy import func

from app import db
from .score import ScoreModel


class PaperModel(db.Model):

    __tablename__ = "papers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    sum_score = db.Column(db.Integer, default=100, nullable=False)
    info = db.Column(db.Text)

    questions = db.relationship('QuestionModel', backref='paper', lazy='dynamic')
    scores = db.relationship('ScoreModel', backref='paper', lazy='dynamic')

    def to_show(self):
        return {
            "id": self.id,
            "name": self.name,
            "exam_date": self.exam_date.strftime('%Y-%m-%d'),
            "sum_score": self.sum_score,
            "teacher_name": self.teacher.name,
            "question_count": self.get_question_count(),
            "info": self.info
        }

    def get_question_count(self):
        questions = self.get_all_question()
        return questions.count()

    def to_show_detail(self):
        res = self.to_show()
        questions = self.get_all_question()
        detail = [question.to_show() for question in questions]
        res["detail"] = detail
        return res

    def get_all_question(self):
        questions = QuestionModel.query.filter_by(paper_id=self.id)
        return questions

    def get_all_score(self):
        scores = ScoreModel.query.filter_by(paper_id=self.id)
        return scores

    def to_show_score(self):
        scores = db.session.query(ScoreModel.student_id, func.sum(ScoreModel.points))\
                           .group_by(ScoreModel.student_id)\
                           .having(ScoreModel.paper_id == self.id).all()

        data = {
            "name": self.name,
            "score_list": scores
        }
        return data


class QuestionModel(db.Model):

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question_num = db.Column(db.Integer)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))
    info = db.Column(db.Text)
    score_in_paper = db.Column(db.Integer)

    score = db.relationship('ScoreModel', backref='question', lazy='dynamic')

    def to_show(self):
        return {"question_num": self.question_num, "score": self.score_in_paper,
                "paper_id": self.paper_id, "info": self.info}