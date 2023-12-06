from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template,request
from dbClass import app,db,Member,Board,Comment
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

if __name__ == '__main__':
    app.run(debug=True)