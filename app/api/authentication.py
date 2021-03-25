from datetime import timedelta, datetime

from flask import request, make_response, abort, current_app, jsonify
from . import api
from ..models import User

from flask_jwt_extended import create_access_token, current_user
from .. import jwtm


@jwtm.user_identity_loader
def user_identity_lookup(user):
    return {
        "user_id": user.id,
        "is_administrator": user.admin_role
    }


@jwtm.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]["user_id"]
    return User.query.filter_by(id=identity).one_or_none()


@api.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        abort(401)

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        abort(404)

    if not user.verify_password(auth.password):
        abort(401)
    
    token = create_access_token(identity=user)

    return jsonify({
        "token": token
    })
