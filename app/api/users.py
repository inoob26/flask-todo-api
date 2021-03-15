from flask import jsonify, request, abort
from . import api
from .. import db
from ..models import User, Todo, UserSchema
from marshmallow.exceptions import ValidationError
from .decorators import validate_request, admin_required
from flask_jwt_extended import jwt_required


@api.route('/user', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    schema = UserSchema(many=True)
    
    output = schema.dump(users)

    return jsonify({'users': output}), 200


@api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)

    return jsonify({
        'user': user.to_json()
    }), 200


@api.route('/user', methods=['POST'])
@validate_request
@admin_required()
def create_user():
    data = request.get_json()
    schema = UserSchema()

    try:
        user = schema.load(data)
        
        exists = User.query.filter_by(username=user['username']).first()
        
        if exists:
            abort(409, {'msg': f'{user["username"]} is already exists'})

        u = User(**user)
        db.session.add(u)
        db.session.commit()
        
        user_id = u.id

    except ValidationError as e:
        raise ValidationError('user data is not valid')

    return jsonify({
        'msg': f"user {user['username']} has been created successfuly",
        'id': user_id
    }), 201
    

@api.route('/user/<int:user_id>', methods=['PUT'])
@validate_request
@admin_required()
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    schema = UserSchema()

    try:
        new_data = schema.load(data)

        user.username = new_data['username']
        user.password = new_data['password']
        user.admin_role = new_data['admin_role']
        
        db.session.add(user)
        db.session.commit()

    except ValidationError as e:
        raise ValidationError('user data is not valid')

    return jsonify({
        'msg': 'user data has been changed'
    })

