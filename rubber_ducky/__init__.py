
from flask_restplus import Api
from flask import Blueprint

from .src.controllers.user_controller import api as user_ns
from .src.controllers.auth_controller import api as auth_ns

user_api = Blueprint('api', __name__)

api = Api(user_api,
        title='Rubber Ducky WebAPI',
        version='1.0',
        description='QnA Application using Flask RESTplus'
    )

api.add_namespace(user_ns, path='/users')
api.add_namespace(auth_ns)
