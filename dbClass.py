from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

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

    # def __repr__(self):
    #     return f'{self.artist} {self.title} 추천 by {self.username}'

class Board(db.Model):
    board_id = db.Column(db.Integer,primary_key=True)
    comment_id = db.Column(db.Integer,nullable=False)
    member_id = db.Column(db.Integer,db.ForeignKey('member.member_id'), nullable=False)
    skill = db.Column(db.String, nullable=False)
    secondTag = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)

    db.relationship('Member')

    # def __repr__(self):
    #     return f'{self.artist} {self.title} 추천 by {self.username}'

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'),nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'),nullable=False)
    content = db.Column(db.String, nullable=False)

    db.relationship('Board')
    db.relationship('Member')
    

    # def __repr__(self):
    #     return f'{self.artist} {self.title} 추천 by {self.username}'

with app.app_context():
    db.create_all()