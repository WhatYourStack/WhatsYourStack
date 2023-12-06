from xml.etree.ElementTree import Comment
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

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
    boards = db.relationship('Board', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'member.member_id'), nullable=True)
    skill = db.Column(db.String, nullable=False)
    secondTag = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    comments = db.relationship('Comment', backref='board', lazy=True)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'member.member_id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey(
        'board.board_id'), nullable=False)
    content = db.Column(db.String, nullable=False)


@app.route('/')
def home():
    board_list = Board.query.all()
    return render_template('index.html', data=board_list)


@app.route('/post/insert', methods=['POST'])
def input_post():
    photo = request.form['photoUrl']
    skill = request.form['skill']
    tags = request.form['tags']
    content = request.form['content']

    board = Board(
        member_id=1,
        comment_id=1,
        skill=skill,
        secondTag=tags,
        content=content,
        image_url=photo
    )
    db.session.add(board)
    db.session.commit()

    return render_template('board.html')
  

@app.route('/post/comment', methods=['POST'])
def input_comment():

    content = request.form['content']

    comment = Comment(
        board_id=3,
        member_id=1,
        content=content,
    )
    db.session.add(comment)
    db.session.commit()

    return render_template('comment.html')


@app.route("/login")
def login():
    member_list = Member.query.all()
    return render_template("login.html", data = member_list)


if __name__ == "__main__":
    app.run(debug=True)
