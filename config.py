class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/wsj/project/ScoreManagementSystem/app.db'
    # 自动保存开启
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    HOST = '0.0.0.0'
    PORT = 80
    DEBUG = True
    SECRET_KEY = 'python123'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
