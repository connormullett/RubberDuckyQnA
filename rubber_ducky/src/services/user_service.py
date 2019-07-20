
import uuid
from datetime import datetime

from rubber_ducky.src import db
from rubber_ducky.src.models.user import User


def create_user(data):

    user = User.query.filter_by(email=data['email']).first()

    if user:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

    username = data.get('username')

    if ' ' in username:
        return {
            'status': 'fail',
            'message': 'Username cannot have spaces'
        }, 400

    new_user = User(
        public_id=uuid.uuid4(),
        email=data.get('email'),
        username=username,
        password=data.get('password'),
        registered_on=datetime.utcnow(),
    )
    save_changes(new_user)
    return generate_token(new_user)


def get_all_users():
    return User.query.all()


def get_a_user(id):
    return User.query.filter_by(id=id).first()


def get_user_by_public_id(public_id):
    return User.query.filter_by(public_id=public_id).first()


def get_user_by_name(username):
    return User.query.filter_by(username=username).first()


def update_user(id, data):
    user = get_a_user(id)
    for key, item in data.items():
        setattr(user, key, item)
    user.modified_at = datetime.utcnow()
    db.session.commit()
    response = {'status': 'updated user'}
    return response, 200


def delete_user(id):
    user = User.query.filter_by(public_id=id).first()
    db.session.delete(user)
    db.session.commit()
    return None, 204


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
    
