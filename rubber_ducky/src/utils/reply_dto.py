
from flask_restplus import Namespace, fields


class ReplyDto:
    api = Namespace('reply', description='replies to answers')
    reply = api.model('reply', {
        'id': fields.Integer(description='replies ID'),
        'content': fields.String(description='content of reply'),
        'owner_id': fields.String(description='owners ID'),
        'answer_id': fields.String(description='ID of the answer'),
        'created_at': fields.DateTime(description='when reply was created at'),
        'modified_at': fields.DateTime(description='revision date of reply')
    })


class ReplyUpdateDto:
    api = ReplyDto.api
    reply = api.model('reply_update', {
        'content': fields.String(description='content of reply')
    })


class ReplyCreateDto:
    api = ReplyDto.api
    reply = api.model('reply_create', {
        'content': fields.String(description='content of reply'),
        'answer_id': fields.Id(description='answers ID')
    })
