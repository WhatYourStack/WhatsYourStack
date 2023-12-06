from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import app

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')


db = SQLAlchemy(app)

class Member(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

class Board(db.Model):
    board_id = db.Column(db.Integer,primary_key=True)
    comment_id = db.Column(db.Integer,db.ForeignKey('comment.comment_id'),nullable=True)
    member_id = db.Column(db.Integer,db.ForeignKey('member.member_id'), nullable=True)
    skill = db.Column(db.String, nullable=False)
    secondTag = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)

    db.relationship('Member')
    db.relationship('Comment')

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'),nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'),nullable=False)
    content = db.Column(db.String, nullable=False)

    db.relationship('Board')
    db.relationship('Member')
    
with app.app_context():
    db.create_all()