
from datetime import datetime

from flask import g

from rubber_ducky.src import db
from rubber_ducky.src.models import user, question, answer


def create_question(data):

    new_question = question.Question(
        title=data['title'],
        question=data['question'],
        owner_id=g.user.get('owner_id'),
        created_at=datetime.utcnow()
    )

    save_changes(new_question)
    return None, 201


def get_all_questions():
    return question.Question.query.all()


def get_question_by_id(id):
    return question.Question.query.filter_by(id=id).first()


def get_questions_by_original_poster_id(owner_id):
    return question.Question.query.filter_by(owner_id=owner_id).all()


def update_question(question_id, data):
    question = question.Question.query.filter_by(id=question_id).first()
    for key, item in data.items():
        setattr(question, key, item)
    db.session.commit()
    return question.Question.query.filter_by(id=question_id)


def delete_question(id):
    question = question.Question.query.filter_by(id=id).first()
    db.session.delete(question)
    db.session.commit()
    return None, 204


def mark_question_best_answer(question_id, answer_id):
    question = question.Question.query.filter_by(id=question_id).first()
    question.best_answer = answer_id
    db.session.commit()
    return {'status': 'question updated successfully'}


def save_changes(data):
    db.session.add(data)
    db.session.commit()
