
from flask import request, g
from flask_restplus import Resource

from ..utils.reply_dto import ReplyDto, ReplyCreateDto, ReplyUpdateDto
from ..services import reply_service
from ..utils.decorator import Authenticate
from .user_controller import parser

api = ReplyDto.api
reply = ReplyDto.api
reply_create = ReplyCreateDto.reply
reply_update = ReplyUpdateDto.reply

@api.route('/')
class ReplyPost(Resource):

    @api.response(201, 'Reply created')
    @api.doc('create new reply')
    @api.expect(reply_create, validate=True)
    @api.expect(parser)
    @Authenticate
    def post(self): 
        data = request.json
        return user_service.create_reply(data)
