from flask import jsonify, request, abort
from . import api
from .. import db
from ..models import Todo, TodoSchema
from flask_jwt_extended import jwt_required
from .decorators import user_required, validate_request
from marshmallow.exceptions import ValidationError


@api.route('/todo')
@jwt_required()
@user_required()
def get_all_todos(user_id):
    todos = Todo.query.filter_by(user_id=user_id).all()

    output = [ todo.to_json() for todo in todos ]
    return jsonify({
        "todos": output
    })


@api.route('/todo', methods=['POST'])
@validate_request
@jwt_required()
@user_required()
def create_todo(user_id):
    data = request.get_json()
    schema = TodoSchema()

    try:
        todo = schema.load(data)
        todo['user_id'] = user_id

        t = Todo(**todo)
        db.session.add(t)
        db.session.commit()

        todo_id = t.id

    except ValidationError:
        raise ValidationError('todo data is not valid')

    return jsonify({
        'msg': f"todo has been created successfuly",
        'id': todo_id
    }), 201


@api.route('/todo/<int:todo_id>', methods=['GET'])
@jwt_required()
@user_required()
def get_todo(user_id, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    
    if not todo:
        abort(404, {'msg': f'todo {todo_id} not found'})

    return jsonify({
        'todo': todo.to_json()
    })


@api.route('/todo/<int:todo_id>', methods=['PUT'])
@jwt_required()
@validate_request
@user_required()
def edit_todo(user_id, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        abort(404, {'msg': f'todo {todo_id} not found'})

    data = request.get_json()
    schema = TodoSchema()

    try:
        new_data = schema.load(data)        
        todo.text = new_data.get('text', todo.text)
        todo.complete = new_data.get('complete', todo.complete)

        db.session.add(todo)
        db.session.commit()

    except ValidationError as e:
        raise ValidationError('todo data is not valid')


    return jsonify({
        'msg': f"todo data has been changed"
    })


@api.route('/todo/<int:todo_id>', methods=['DELETE'])
@jwt_required()
@user_required()
def delete_todo(user_id, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        abort(404, {'msg': f'todo {todo_id} not found'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({
        'msg': f"todo has been deleted"
    })
