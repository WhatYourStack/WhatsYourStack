from flask import Flask, render_template,request
import dbClass
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
      'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/post/insert', methods=['POST'])
def input_post():
   photo = request.form['photoUrl']
   skill = request.form['skill']
   tags = request.form['tags']
   content = request.form['content']

   song = dbClass.Board(
      comment_id = 1,
      member_id =1,
      skill=skill, 
      secondTag=tags,
      content=content, 
      image_url=photo
      )
   db.session.add(song)
   db.session.commit()

   return render_template('index.html')

@app.route('/mypage')
def mypage():
	return 'This is My page!'

if __name__ == "__main__":
   app.run(debug=True)