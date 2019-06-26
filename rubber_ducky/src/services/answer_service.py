
from datetime import datetime

from flask import g

from rubber_ducky.src import db
from rubber_ducky.src.models import user, question, answer


def get_answer_by_id(answer_id):
    return answer.Answer.query.filter_by(id=answer_id).first()
