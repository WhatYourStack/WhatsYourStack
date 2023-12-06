from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template,request,jsonify
from dbClass import app,Member
import re
app = Flask(__name__)

DATABASE_URL = "sqlite:///database.db"

from sqlalchemy.orm import declarative_base
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)

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

if __name__ == '__main__':
    app.run(debug=True)