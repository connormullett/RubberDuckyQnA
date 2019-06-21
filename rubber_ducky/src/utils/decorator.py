
from functools import wraps
from flask import request, g

from rubber_ducky.src.services.auth_service import Auth


def Authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        
        token = data.get('data')

        if not token:
            return data, status

        g.user = {'owner_id': data['data']['user_id']}
        return f(*args, **kwargs)

    return decorated


def AdminAuthenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated