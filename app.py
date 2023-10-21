from flask import Flask, request
import requests
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VERY VERY SECRET KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:password@db/postgres'
db = SQLAlchemy(app)
# Если таблицы еще нет - создаем
from models import Question
with app.app_context():
    db.create_all()
    db.session.commit()


def get_last_saved_question():
    all_questions = db.session.query(Question.question).all()
    if len(all_questions) != 0:
        return all_questions[-1][0]
    else:
        return []


@app.route('/api/questions', methods=['POST'])
def questions():
    last_question = get_last_saved_question()
    params = request.get_json(force=True)
    response = requests.get(f'https://jservice.io/api/random?count={params["question_num"]}').json()
    for question in response:
        while db.session.query(db.exists().where(Question.id_question == question['id'])).scalar():
            new_response = requests.get('https://jservice.io/api/random?count=1').json()
            question = new_response[0]
        db.session.add(Question(id_question=question['id'], question=question['question'],
                                answer=question['answer'], creation_date=question['created_at']))
        db.session.commit()
    return last_question


if __name__ == '__main__':
	app.run()
