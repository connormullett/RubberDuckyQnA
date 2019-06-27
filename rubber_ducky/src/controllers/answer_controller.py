
from flask import request, g
from flask_restplus import Resource

from ..utils.answer_dto import AnswerDto, AnswerCreateDto, AnswerUpdateDto, AnswerDetailDto
from ..utils.decorator import Authenticate
from ..services import question_service, answer_service, user_service

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
    @Authenticate
    def delete(self, answer_id):
        user_id = user_service.get_a_user(g.user.get('owner_id')).public_id
        answer = answer_service.get_answer_by_id(answer_id)
        if not answer:
            api.abort(404)
        if user_id != answer.owner_id:
            api.abort(401)
        return answer_service.delete_answer(answer_id)
