
from flask_restplus import Namespace, fields


class UserDto:  # List item
    api = Namespace('user', description='user related ops')
    user = api.model('user', {
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(required=True, description='users id')
    })


class UserDetailDto:
    api = UserDto.api
    user = api.model('user_detail', {
        'public_id': fields.String(required=True, description='users id'),
        'username': fields.String(required=True, description='user username'),
        'registered_on': fields.DateTime(description='time of registration'),
        'modified_at': fields.DateTime(description='time of revision'),
    })


class UserMe:
    api = UserDto.api
    user = api.model('user_detail', {
        'email': fields.String(required=True, description='users email'),
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(required=True, description='users id'),
        'registered_on': fields.DateTime(description='time of registration'),
        'modified_at': fields.DateTime(description='time of revision'),
    })
    


class UserCreateDto:
    api = UserDto.api
    user = api.model('user_create', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'confirm_password': fields.String(required=True, description='users confirmation of password')
    })


class UserUpdateDto:
    api = UserDto.api
    user = api.model('user_update', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
    })
