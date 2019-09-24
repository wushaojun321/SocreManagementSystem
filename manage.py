import sys

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import student, teacher, score, classes, papers, others

from app import db
from app import app as cur_app

migrate = Migrate(cur_app, db)

manager = Manager(cur_app)
manager.add_command('db', MigrateCommand)

sys.path.append(".")


if __name__ == '__main__':
    manager.run()