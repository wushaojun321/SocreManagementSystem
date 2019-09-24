from app import db


class StudentModel(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    student_id = db.Column(db.String(20), unique=True)
    student_class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

    score = db.relationship('ScoreModel', backref='student', lazy='dynamic')

    def to_show(self):
        res = {"id": self.id, "name": self.name, "student_id": self.student_id, "class_name": self.student_class.name}
        return res
