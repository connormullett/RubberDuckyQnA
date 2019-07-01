
from flask_restplus import Api
from flask import Blueprint

from .src.controllers.user_controller import api as user_ns
from .src.controllers.auth_controller import api as auth_ns
from .src.controllers.question_controller import api as question_ns
from .src.controllers.answer_controller import api as answer_ns
from .src.controllers.reply_controller import api as reply_ns

user_api = Blueprint('api', __name__)

api = Api(user_api,
        title='Rubber Ducky WebAPI',
        version='1.0',
        description='QnA Application using Flask RESTplus'
    )

api.add_namespace(user_ns, path='/api/v1/users')
api.add_namespace(auth_ns, path='/api/v1/auth')
api.add_namespace(question_ns, path='/api/v1/questions')
api.add_namespace(answer_ns, path='/api/v1/answers')
api.add_namespace(reply_ns, path='/api/v1/replies')
