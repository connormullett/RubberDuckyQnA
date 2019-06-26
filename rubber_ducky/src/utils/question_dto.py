
from flask_restplus import Namespace, fields


class QuestionDto:  # List Item
    api = Namespace('question', description='the \'forum\' entity of the app')
    question = api.model('question', {
        'id': fields.Integer(required=True, description='unique id of post'),
        'title': fields.String(required=True, description='title of post'),
        'owner_id': fields.String(required=True, description='owners id'),
        'created_at': fields.DateTime(required=True, description='when question was created')
    })


class QuestionCreate:
    api = QuestionDto.api
    question = api.model('question_create', {
        'title': fields.String(required=True, description='title of post'),
        'question': fields.String(required=True, description='the question being asked')
    })


class QuestionUpdate:
    api = QuestionDto.api
    question = api.model('question_update', {
        'title': fields.String(required=True, description='title of post'),
        'question': fields.String(required=True, description='the question being asked'),
        'best_answer': fields.Integer(description='only done when changing best answer')
    })


class QuestionDetail:
    api = QuestionDto.api
    question = api.model('question_update', {
        'title': fields.String(required=True, description='title of post'),
        'question': fields.String(required=True, description='the question being asked'),
        'owner_id': fields.String(required=True, description='owners_id'),
        'best_answer': fields.Integer(description='only done when changing best answer'),
        'created_at': fields.DateTime(description='when question was asked'),
        'modified_at': fields.DateTime(description='when question was last modified'),
        # Answers DTO here?
    })
