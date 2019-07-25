
import werkzeug
import os

from flask import request, g
from flask_restplus import Resource, reqparse
from flask_restplus import marshal

from ..utils.decorator import Authenticate
from ..utils.user_dto import (UserDto, UserCreateDto, 
    UserDetailDto, UserUpdateDto, UserMe)

from ..services import user_service

api = UserDto.api
user = UserDto.user
user_create = UserCreateDto.user
user_detail = UserDetailDto.user
user_update = UserUpdateDto.user
user_me = UserMe.user

parser = api.parser()
parser.add_argument('Authorization', location='headers', 
    help="Authorization token")
parser.add_argument('limit', type=int, help='how many objects to return')
parser.add_argument('start', type=int, help='id to start query')
parser.add_argument('end', type=int, help='when to end the query')
parser.add_argument('next', type=int, help='next page')
parser.add_argument('prev', type=int, help='previous page')


@api.route('/')
class UserList(Resource):

    @api.response(201, 'User created')
    @api.doc('create new user')
    @api.expect(user_create, validate=True)
    def post(self):
        data = request.json
        return user_service.create_user(data=data)

    @api.doc('get all users')
    @api.expect(parser)
    @Authenticate
    def get(self):
        args = parser.parse_args()
        if not args.get('limit'):
            query = user_service.get_all_users()
            return marshal(query, user), 200
        else:
            return {'status': 'Not implemented'}, 403
            query = user_service.get_paginated_users(args)
            print(query.items)
            obj = {
                'next_page': query.next_num,
                'page': query.page,
                'data': marshal(query.items, user)
            }
            return obj, 200


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
    @api.marshal_with(user_me, skip_none=True)
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
        image = user_service.get_profile_picture(name)
        print(image)
        return {'image': image[0]['body'].read()}

