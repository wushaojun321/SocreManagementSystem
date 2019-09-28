from app import db
from .student import StudentModel


class ClassModel(db.Model):

    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    students = db.relationship('StudentModel', backref='student_class', lazy='dynamic')
    info = db.Column(db.Text)

    def to_show(self):
        students = self.get_all_students()
        res = {
            "id": self.id,
            "class_name": self.name,
            "student_count": students.count(),
            "info": self.info
        }
        return res

    def get_all_students(self):
        students = StudentModel.query.filter_by(student_class_id=self.id)
        return students

    def to_show_detail(self):
        res = self.to_show()
        students = self.get_all_students()
        res["data"] = [student.to_show() for student in students]
        return res