import pandas as pd
from app import db


class ScoreModel(db.Model):

    __tablename__ = "score"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    points = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_score_detail(cls, paper):
        scores = cls.query.filter_by(paper_id=paper.id)
        columns_question = [i for i in range(paper.get_question_count())]
        columns = ["student_id", "student_name", "class_name"] + columns_question
        df = pd.DataFrame(columns=columns)
        for score in scores:
            cur_index_list = df[df["student_id"] == score.student.student_id].index.tolist()

            if not cur_index_list:
                df = df.append({
                    "student_id": score.student.student_id,
                    "student_name": score.student.name,
                    "class_name": score.student.student_class.name
                }, ignore_index=True)
                df.index = range(df.shape[0])
                cur_index = max(df.index.tolist())
            else:
                cur_index = cur_index_list[0]
            df.loc[cur_index, ["student_id", "student_name", "class_name"]] = [
                score.student.student_id,
                score.student.name,
                score.student.student_class.name,
                ]
            df.loc[cur_index, score.question.question_num] = score.points
        df.sort_index(by=["class_name", "student_id"])
        df.index = range(df.shape[0])
        res_dict = df.T.to_dict()
        res_list = [0 for i in range(len(res_dict))]
        for k, v in res_dict.items():
            res_list[k] = v
        return res_list
