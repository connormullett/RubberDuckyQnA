
from flask import request, g
from flask_restplus import Resource

from ..utils.answer_dto import AnswerDto, AnswerCreateDto, AnswerUpdateDto, AnswerDetailDto
from ..utils.decorator import Authenticate
from ..services import question_service, answer_service, user_service

from .user_controller import parser

api = AnswerDto.api
answer = AnswerDto.answer
answer_create = AnswerCreateDto.answer
answer_update = AnswerUpdateDto.answer
answer_detail = AnswerDetailDto.answer


@api.route('/')
class AnswerList(Resource):

    @api.response(201, 'Answer Created')
    @api.doc('post answer')
    @api.expect(answer_create, validate=True)
    @api.expect(parser)
    @Authenticate
    def post(self):
        data = request.json
        return answer_service.create_answer(data)

    @api.doc('get all answers')
    @api.marshal_list_with(answer)
    def get(self):
        return answer_service.get_all_answers()
    

@api.route('/<answer_id>')
@api.response(404, 'answer not found')
class Answer(Resource):

    @api.doc('get an answer by id')
    @api.marshal_with(answer_detail)
    def get(self, answer_id):
        return answer_service.get_answer_by_id(answer_id)

    @api.doc('update answer')
    @api.expect(answer_update, validate=True)
    @api.expect(parser)
    @api.marshal_with(answer_detail)
    @Authenticate
    def put(self, answer_id):
        data = request.json
        user_id = user_service.get_a_user(g.user.get('owner_id')).public_id
        answer = answer_service.get_answer_by_id(answer_id)
        if not answer:
            api.abort(404)
        if user_id != answer.owner_id:
            api.abort(401)
        return answer_service.update_answer(answer_id, data)
    
    @api.doc('delete answer')
    @api.expect(parser)
    @Authenticate
    def delete(self, answer_id):
        user_id = user_service.get_a_user(g.user.get('owner_id')).public_id
        answer = answer_service.get_answer_by_id(answer_id)
        if not answer:
            api.abort(404)
        if user_id != answer.owner_id:
            api.abort(401)
        return answer_service.delete_answer(answer_id)


@api.route('/by_question/<question_id>')
@api.param('question_id', 'id of the question to search answers for')
@api.response(404, 'question not found')
class AnswerByQuestion(Resource):

    @api.doc('get questions by id')
    @api.marshal_list_with(answer)
    @api.expect(parser)
    @Authenticate
    def get(self, question_id):

        question = question_service.get_question_by_id(question_id)

        if not question:
            api.abort(404)
        
        return answer_service.get_answers_by_question_id(question_id)
