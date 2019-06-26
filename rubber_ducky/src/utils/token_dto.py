
from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='authentication')
    user_auth = api.model('auth_login', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })