
from flask import request, g
from flask_restplus import Resource

from ..utils.question_dto import QuestionDto, QuestionCreate, QuestionDetail, QuestionUpdate
from ..utils.decorator import Authenticate
from ..services import question_service, answer_service, user_service

api = QuestionDto.api
question = QuestionDto.question
question_create = QuestionCreate.question
question_update = QuestionUpdate.question
question_detail = QuestionDetail.question


@api.route('/')
class QuestionList(Resource):

    @api.response(201, 'Question Created')
    @api.doc('create question')
    @api.expect(question_create, validate=True)
    @Authenticate
    def post(self):
        data = request.json
        return question_service.create_question(data)
    
    @api.doc('get all questions')
    @api.marshal_list_with(question)
    def get(self):
        return question_service.get_all_questions()


@api.route('/<question_id>')
@api.param('question_id', 'questions id')
@api.response(404, 'question not foumd')
@api.response(401, 'unauthorized')
class Question(Resource):

    @api.doc('get question by Id')
    @api.marshal_with(question_detail)
    def get(self, question_id):
        return question_service.get_question_by_id(question_id)


    @api.doc('update question')
    @api.expect(question_update, validate=True)
    @api.marshal_with(question_detail)
    @Authenticate
    def put(self, question_id):
        data = request.json
        user_id = user_service.get_a_user(g.user.get('owner_id')).public_id
        question = question_service.get_question_by_id(question_id)
        if not question:
            api.abort(404)
        if user_id != question.owner_id:
            api.abort(401)
        return question_service.update_question(question_id, data)
    
    @api.doc('delete question by ID')
    @Authenticate
    def delete(self, question_id):
        user_id = user_service.get_a_user(g.user.get('owner_id')).public_id
        if user_id != question_service.get_question_by_id(question_id).owner_id:
            api.abort(401)
        return question_service.delete_question(question_id)


@api.route('/<question_id>/best_answer/<answer_id>')
@api.param('question_id', 'id of question')
@api.param('answer_id', 'new best answer\'s id')
@api.response('404', 'answer or question not found')
@api.response('401', 'unauthorized')
class QuestionAdjustment(Resource):

    @api.doc('change questions best_answer property to answer_id')
    @Authenticate
    def post(question_id, answer_id):
        if g.user.get('owner_id') != question_service.get_question_by_id(question_id).owner_id:
            api.abort(401)
        if not answer_service.get_answer_by_id(answer_id):
            api.abort(404)
        return question_service.mark_question_best_answer(question_id, answer_id)
