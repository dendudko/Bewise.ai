from app import db


class Question(db.Model):
    __tablename__ = "questions"
    id_question = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    creation_date = db.Column(db.DateTime)
