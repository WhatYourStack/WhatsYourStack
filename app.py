from xml.etree.ElementTree import Comment
from flask import Flask, render_template,request,jsonify,redirect
# import dbClass
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
import os, re
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
      'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Member(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    boards = db.relationship('Board', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'), nullable=True)
    skill = db.Column(db.String, nullable=False)
    secondTag = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    comments = db.relationship('Comment', backref='board', lazy=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)
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
      comment_id = 1,
      member_id =1,
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
      board_id = 3,
      member_id =1,
      content=content, 
   
      )
   db.session.add(comment)
   db.session.commit()

   return render_template('comment.html')

@app.route('/login')
def login():
   return render_template('login.html')

engine = create_engine('sqlite:///' + os.path.join(basedir, 'database.db'), echo=True)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        email = data.get('email')
        raw_password = data.get('password')
        name = data.get('name')

        if not is_valid_email(email):
            return jsonify({'message' : '올바른 메일 형식이 아닙니다.'})
        
        hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

        new_member = Member(email=email, password=hashed_password, name=name)
        session.add(new_member)
        try:
            session.commit()
            print("회원가입이 완료되었습니다.")
            return redirect('/login')
        except IntegrityError as e:
            session.rollback()
            print(f"무결성 제약 조건 위반이 발생했습니다: {e}")
            return jsonify({'message': '중복된 이메일 주소입니다.'})
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