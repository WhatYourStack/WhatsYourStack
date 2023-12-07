from xml.etree.ElementTree import Comment

from flask import Flask, render_template,request,jsonify,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import os, re
from sqlalchemy import create_engine
from sqlalchemy import func

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class Member(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    boards = db.relationship('Board', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'member.member_id'), nullable=True)
    skill = db.Column(db.String, nullable=False)
    secondTag = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    # comments = db.relationship('Comment', backref='comment', lazy=True)


# class Comment(db.Model):
#     comment_id = db.Column(db.Integer, primary_key=True)
#     member_id = db.Column(db.Integer, db.ForeignKey(
#         'member.member_id'), nullable=False)
#     board_id = db.Column(db.Integer, db.ForeignKey(
#         'board.board_id'), nullable=False)
#     content = db.Column(db.String, nullable=False)


@app.route('/')
def home():
    board_list = Board.query.all()
    return render_template('index.html', data=board_list)

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '').lower()
    if search_query:
        search_pattern = f"%{search_query}%"
        results = Board.query.filter(func.lower(Board.skill).like(search_pattern)).all()

        if results:
            return render_template('search_results.html', boards=results)
        else:
            return render_template('search_results.html', message="검색 결과가 없습니다.")
    else:
        return redirect(url_for('home'))

@app.route('/post/insert', methods=['GET', 'POST'])
def input_post():
    if request.method == 'POST':
        photo = request.form['photoUrl']
        skill = request.form['skill']
        tags = request.form['tags']
        content = request.form['content']

        board = Board(
            member_id=1,
            skill=skill,
            secondTag=tags,
            content=content,
            image_url=photo
        )
        db.session.add(board)
        db.session.commit()
        return redirect(url_for('home'))
    else:
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


engine = create_engine('sqlite:///' + os.path.join(basedir, 'database.db'), echo=True)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not is_valid_email(email):
            return jsonify({'message' : '올바른 메일 형식이 아닙니다.'})
        
        new_member = Member(email=email, password=password, name=name)
        session.add(new_member)
        try:
            session.commit()
            print("회원가입이 완료되었습니다.")
        except Exception as e:
            session.rollback()
            print(f"에러 발생: {e}")
        finally:
            session.close()

    return render_template('register.html')

def is_valid_email(email):
    pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(pattern, email))

if __name__ == "__main__":
    app.run(debug=True)
