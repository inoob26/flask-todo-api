from . import api
from flask import jsonify, make_response
from marshmallow.exceptions import ValidationError


def bad_request(msg):
    response = jsonify({
        'error': 'bad request', 
        'msg': msg
    })
    response.status_code = 400
    return response


@api.errorhandler(400)
def bad_request_handler(e):
    return bad_request(e.description['msg'])


@api.errorhandler(401)
def unauthorized(e):
    response = jsonify({
        'error': 'Unauthorized',
        'msg': 'Could not verify user'
    })
    
    response.headers['WWW-Authenticate'] = 'Basic realm="Login required!"'
    response.status_code = 401
    
    return response


@api.errorhandler(403)
def forbidden(e):
    response = jsonify({
        'error': 'Forbidden',
        'msg': e.description['msg']
    })
    response.status_code = 403
    
    return response


@api.errorhandler(404)
def not_found(e):
    if not e.description['msg']:
        response = jsonify({
            'error': 'Not found'
        })
    else:
        response = jsonify({
            'msg': e.description['msg']
        })
    
    response.status_code = 404
    
    return response


@api.errorhandler(409)
def conflict(e):
    response = jsonify({
        'error': 'Conflict', 
        'msg': e.description['msg']
    })
    response.status_code = 409
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    print(e)
    return bad_request(e.args[0])
