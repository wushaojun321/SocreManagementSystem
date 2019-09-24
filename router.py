
def router_init():
    from app import api
    from app.resources.teacher import TeacherListView, TeacherView
    from app.resources.other import TokenView
    from app.resources.classes import ClassListView, ClassView
    from app.resources.student import StudentListView, StudentView
    from app.resources.papers import PaperListView, PaperView
    from app.resources.score import PaperScoreView
    api.add_resource(TeacherListView, '/teacherList')
    api.add_resource(TeacherView, '/teacher/<int:teacher_id>')
    api.add_resource(TokenView, '/token')
    api.add_resource(PaperListView, '/paperList')
    api.add_resource(PaperView, '/paper/<int:paper_id>')
    api.add_resource(ClassListView, '/classList')
    api.add_resource(ClassView, '/class/<int:class_id>')
    api.add_resource(StudentListView, '/studentList')
    api.add_resource(StudentView, '/student/<int:id>')
    api.add_resource(PaperScoreView, '/paperScore')