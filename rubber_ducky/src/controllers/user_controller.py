
import werkzeug
import os

from flask import request, g
from flask_restplus import Resource, reqparse

from ..utils.user_dto import (UserDto, UserCreateDto, 
    UserDetailDto, UserUpdateDto, UserMe)
from ..services import user_service
from ..utils.decorator import Authenticate

api = UserDto.api
user = UserDto.user
user_create = UserCreateDto.user
user_detail = UserDetailDto.user
user_update = UserUpdateDto.user
user_me = UserMe.user

parser = api.parser()
parser.add_argument('Authorization', location='headers')


@api.route('/')
class UserList(Resource):

    @api.response(201, 'User created')
    @api.doc('create new user')
    @api.expect(user_create, validate=True)
    def post(self):
        data = request.json
        return user_service.create_user(data=data)

    @api.doc('get all users')
    @api.marshal_list_with(user)
    @api.expect(parser)
    @Authenticate
    def get(self):
        return user_service.get_all_users()


@api.route('/me')
@api.response(401, 'unauthorized')
@api.expect(parser)
class UserMe(Resource):

    @api.doc('update users account')
    @api.expect(user_update)
    @Authenticate
    def put(self):
        data = request.json
        user_id = g.user.get('owner_id')
        return user_service.update_user(user_id, data)

    @api.doc('get account associated with token')
    @api.marshal_with(user_me)
    @Authenticate
    def get(self):
        user_id = g.user.get('owner_id')
        return user_service.get_a_user(user_id)

    @api.doc('delete account')
    @Authenticate
    def delete(self):
        user_id = g.user.get('owner_id')
        return user_service.delete_user(user_id)


@api.route('/by_name/<username>')
@api.param('username', 'users unique name')
@api.response(404, 'user not found')
class UserByName(Resource):

    @api.doc('get user by name')
    @api.marshal_with(user_detail)
    def get(self, username):
        return user_service.get_user_by_name(username)


@api.route('/by_public_id/<public_id>')
@api.param('public_id', 'users public ID')
@api.response(404, 'user not found')
class UserByPublicId(Resource):

    @api.doc('get user by public id')
    @api.marshal_with(user_detail)
    def get(self, public_id):

        # TODO: marshal function to prevent null JSON

        response = user_service.get_user_by_public_id(public_id)
        print(response)
        if not response:
            return {'status': 'user not found'}, 404
        return response


@api.route('/image')
class ProfilePicture(Resource):

    @api.doc('upload an image as your profile pic')
    @Authenticate
    def post(self):
        if 'file' not in request.files:
            return {'status': 'no file supplied'}, 400
        image = request.files['file']
        return user_service.upload_profile_picture(image)

    
@api.route('/image/<name>')
@api.param('name', 'users unique name')
class ProfilePictureRetrieve(Resource):

    @api.doc('get profile picture by username')
    def get(self, name):
        # image = user_service.get_profile_picture(name)
        return {'status': 'not implemented'}

