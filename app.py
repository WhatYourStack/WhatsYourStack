from xml.etree.ElementTree import Comment
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
import os
import re
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

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
    boards = db.relationship('Board', backref='board', lazy=True)
    # comments = db.relationship('Comment', backref='author', lazy=True)


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'member.member_id'), nullable=True)
    skill = db.Column(db.String, nullable=False)
    secondTag = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    # comments = db.relationship('Comment', backref='comment', lazy=True)


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


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '').lower()
    if search_query:
        search_pattern = f"%{search_query}%"
        results = Board.query.filter(func.lower(
            Board.skill).like(search_pattern)).all()

        if results:
            return render_template('search_results.html', boards=results)
        else:
            return render_template('search_results.html', message="검색 결과가 없습니다.")
    else:
        return redirect(url_for('home'))


@app.route('/member/edit', methods=['POST'])
def edit_post():

    board_receive = request.form['board_id']
    email_receive = request.form['email']
    skill_receive = request.form['skill']
    secondTag_receive = request.form['secondTag']
    content_receive = request.form['content']

    print(board_receive, email_receive, skill_receive,
          secondTag_receive, content_receive)
    return render_template('index.html')


@app.route('/member/<int:id>')
def select_post(id):

    board_list = session.query(Board, Member).join(
        Member).filter_by(member_id=id).all()

    return render_template('board.html', data=board_list)


@app.route('/member/delete/<int:member_id>', methods=['POST'])
def delete_post(member_id):

    argId = member_id

    Board.query.filter_by(member_id=argId).delete()
    print(member_id)
    # db.session.commit()

    return home()


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
        return render_template('write.html')


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Check if the entered credentials are valid
        user = Member.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Successful login
            response = {"success": True}
        else:
            # Failed login
            response = {"success": False}

        return jsonify(response)

    # For GET requests, render the login form
    member_list = Member.query.all()
    return render_template("login.html", data=member_list)


engine = create_engine(
    'sqlite:///' + os.path.join(basedir, 'database.db'), echo=True)

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
            return jsonify({'message': '올바른 메일 형식이 아닙니다.'})

        hashed_password = bcrypt.generate_password_hash(
            raw_password).decode('utf-8')

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
    app.run('0.0.0.0', port=5001, debug=True)
