
from datetime import datetime

from flask import g

from rubber_ducky.src import db
from rubber_ducky.src.models import user, question, answer
from rubber_ducky.src.services import user_service, question_service


def create_answer(data):

    user = user_service.get_a_user(g.user.get('owner_id'))
    q = question_service.get_question_by_id(data['question_id'])

    if not q:
        return {'status': 'question does not exist'}, 400

    new_answer = answer.Answer(
        owner_id=user.public_id,
        created_at=datetime.utcnow(),
        content=data['content'],
        question_id=data['question_id']
    )
    save_changes(new_answer)
    return {'status': 'created'}


def get_answers_by_question_id(question_id):
    return answer.Answer.query.filter_by(question_id=question_id).all()


def get_answer_by_id(answer_id):
    return answer.Answer.query.filter_by(id=answer_id).first()


def get_all_answers():
    return answer.Answer.query.all()


def update_answer(answer_id, data):
    a = answer.Answer.query.filter_by(id=answer_id).first()
    for key, item in data.items():
        setattr(a, key, item)
    a.modified_at = datetime.utcnow()
    db.session.commit()
    return answer.Answer.query.filter_by(id=answer_id).first()


def delete_answer(answer_id):
    a = answer.Answer.query.filter_by(id=answer_id).first()
    question_with_best_answer = question.Question.query.filter_by(best_answer=a.id).first()
    if question_with_best_answer.best_answer:
        question_with_best_answer.best_answer = None
    db.session.delete(a)
    db.session.commit()
    return None, 204


def save_changes(data):
    db.session.add(data)
    db.session.commit()
