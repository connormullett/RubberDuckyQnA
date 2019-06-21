
import datetime

from .. import db


class Question(db.Model):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    question = db.Column(db.String(128), nullable=False)
    original_poster = db.Column(db.String, db.ForeignKey('users.public_id'), nullable=False)
    best_answer = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime)
    answers = db.relationship('Answer', backref='questions', cascade='all, delete-orphan', lazy=True)
