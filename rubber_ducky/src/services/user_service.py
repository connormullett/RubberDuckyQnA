
import uuid, re
from datetime import datetime

from rubber_ducky.src import db
from rubber_ducky.src.models.user import User


def create_user(data):

    user = User.query.filter_by(email=data['email']).first()

    if data.get('password') != data.get('confirm_password'):
        return {'status': 'password mismatch'}, 400
    
    if not _check_password_requirements(data.get('password')):
        return {
            'status': 'Password must be between 6 and 20 characters, ' \
            'contain atleast one uppercase and lowercase characters, ' \
            'a number, and must have at least one special symbol'
        }, 400

    if not user:
        new_user = User(
            public_id=uuid.uuid4(),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.utcnow(),
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


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


def _check_password_requirements(password):
    pattern = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')
    match = re.search(pattern, password)
    
    if match:
        return True
    