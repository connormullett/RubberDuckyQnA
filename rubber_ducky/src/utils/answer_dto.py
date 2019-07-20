
from flask_restplus import Namespace, fields


class AnswerDto:
    api = Namespace('answer', description='answers to questions')
    answer = api.model('answer', {
        'id': fields.Integer(required=True, description='unique id of answer'),
        'content': fields.String(required=True, description='body of the answer'),
        'owner_id': fields.String(required=True, description='owners public id'),
        'created_at': fields.DateTime(required=True, description='when answer was created'),
        'question_id': fields.Integer(required=True, description='id of question')
    })


class AnswerCreateDto:
    api = AnswerDto.api
    answer = api.model('answer_create', {
        'content': fields.String(required=True, description='body of the answer'),
        'question_id': fields.Integer(required=True, description='id of question')
    })


class AnswerUpdateDto:
    api = AnswerDto.api
    answer = api.model('answer_update', {
        'content': fields.String(required=True, description='body of the answer')
    })


class AnswerDetailDto:
    api = AnswerDto.api
    answer = api.model('answer_detail', {
        'id': fields.Integer(required=True, description='unique id of answer'),
        'content': fields.String(required=True, description='body of the answer'),
        'owner_id': fields.String(requirend=True, description='owners public id'),
        'created_at': fields.DateTime(required=True, description='when answer was created'),
        'modified_at': fields.DateTime(required=True, description='last revision date of answer'),
        'question_id': fields.Integer(required=True, description='id of question')
    })
