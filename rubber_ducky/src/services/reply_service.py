
from datetime import datetime

from flask import g

from .user_service import save_changes

from rubber_ducky.src import db
from rubber_ducky.src.models import user, reply
from rubber_ducky.src.services import user_service, answer_service


def create_reply(data):

    user = user_service.get_a_user(g.user.get('owner_id'))
    a = answer_service.get_answer_by_id(data['answer_id'])

    if not a:
        return {'status': 'answer does not exist'}, 400

    new_reply = reply.Reply(
        owner_id=user.public_id,
        created_at=datetime.utcnow(),
        content=data['content'],
        answer_id=data['answer_id']
    )

    save_changes(new_reply)
    return {'status': 'created'}
