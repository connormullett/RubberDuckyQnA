
from functools import wraps
from flask import request, g

from rubber_ducky.src.services.auth_service import Auth


def Authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)

        if not data:
            return {'status': 'unauthorized'}
        
        token = data.get('data')

        if not token:
            return data, status

            print(data['data']['user_id'])

        g.user = {'owner_id': data['data']['user_id']}
        return f(*args, **kwargs)

    return decorated
