import app

db = app.db

class Member(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    boards = db.relationship('Board', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'), nullable=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'), nullable=True)
    skill = db.Column(db.String, nullable=False)
    secondTag = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    comments = db.relationship('Comment', backref='board', lazy=True,foreign_keys='Comment.board_id')

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)
    content = db.Column(db.String, nullable=False)

# Flask 앱 컨텍스트 안에서 데이터베이스를 생성합니다.
with app.app_context():
    db.create_all()
