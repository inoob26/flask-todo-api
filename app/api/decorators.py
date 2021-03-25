from flask import request, jsonify, abort
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from .. import jwtm


def validate_request(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not request.is_json:
            abort(400, {'msg': 'mimetype is not valid'})
        return f(*args, **kwargs)    
    return decorator


def admin_required():
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if not claims['sub']['is_administrator']:
                abort(403, {'msg': 'admin permission required'})
            
            return f(*args, **kwargs)
        return decorator
    return wrapper


def user_required():
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            if not claims['sub']['user_id']:
                abort(403, {'msg': 'user_id required'})

            return f(claims['sub']['user_id'], *args, **kwargs)
        return decorator
    return wrapper
