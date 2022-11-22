from datetime import datetime, timedelta
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os
import config

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.DB_LOGIN}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app_root = os.path.dirname(os.path.abspath(__file__))


# DB Model USER
class Users(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    login = db.Column(db.String(200), nullable=True)
    # json structure {'status': (yes, no), 'filter': {}}
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

# DB model Objects
class Tasks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    author = db.Column(db.String(200), db.ForeignKey('users.id'), nullable=False)
    executor = db.Column(db.String(200), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text(), nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

with app.app_context():
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JSON_AS_ASCII'] = False
    
    db.create_all()
    
    # Session(app)