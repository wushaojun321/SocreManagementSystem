from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_restful import Api
from flask_httpauth import HTTPTokenAuth
from router import router_init


auth = HTTPTokenAuth()

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db.init_app(app)
router_init()
