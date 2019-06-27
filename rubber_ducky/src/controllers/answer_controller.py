
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
