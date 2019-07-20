
import uuid, re, os
import boto3
from datetime import datetime

from flask import request, g
from rubber_ducky.src import db
from rubber_ducky.src.models.user import User

from werkzeug.utils import secure_filename


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

    username = data.get('username')

    if ' ' in username:
        return {
            'status': 'fail',
            'message': 'Username cannot have spaces'
        }, 400
        return response_object, 409

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


def upload_profile_picture(image):
    user = get_a_user(g.user.get('owner_id'))

    bucket_url = os.environ.get('BUCKET_URL')
    content_type = request.mimetype
    client = boto3.client('s3',
        endpoint_url=bucket_url,
        aws_access_key_id=os.environ.get('ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('SECRET_KEY'))
    
    filename = user.username

    client.put_object(Body=image,
        Bucket=os.environ.get('BUCKET_NAME'),
        Key=filename,
        ContentType=content_type
    )

    user.has_profile_picture = True
    db.session.commit()

    return {'status': 'uploaded complete'}, 200


def get_profile_picture(name):
    user = get_user_by_name(name)

    if not user:
        return {'status': 'user not found'}

    if not user.has_profile_picture:
        name = 'default.jpg'
    
    bucket_url = os.environ.get('BUCKET_URL')
    content_type = request.mimetype
    client = boto3.client('s3',
        endpoint_url=bucket_url,
        aws_access_key_id=os.environ.get('ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('SECRET_KEY'))
    
    response = client.get_object(
        Bucket=os.environ['BUCKET_NAME'],
        Key=name)

    return {'body': response['Body']}, 200
    

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
    
