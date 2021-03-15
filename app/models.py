from . import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields, validate


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(name='id', type_=db.Integer, primary_key=True)
    username = db.Column(name='username', type_=db.String(64), unique=True)
    password_hash = db.Column(name='password', type_=db.String(128))
    admin_role = db.Column(name='admin_role', type_=db.Boolean, default=False)
    todos = db.relationship("app.models.Todo", backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'admin_role': self.admin_role
        }

    def __repr__(self):
        return f"<User>: id: {self.id}, username: {self.username}, admin {self.admin_role}"


class UserSchema(ma.Schema):
    class Meta:
        model = User

    id = fields.Integer(required=False)
    username = fields.String(required=True, validate=[validate.Length(max=64)])
    password = fields.String(required=True, validate=[validate.Length(max=80)])
    admin_role = fields.Boolean(required=False)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(name='id', type_=db.Integer, primary_key=True)
    text = db.Column(name='text', type_=db.String(50))
    complete = db.Column(name='complete', type_=db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'complete': self.complete
        }

    def __repr__(self):
        return f"<Todo>: id: {self.id}, text: {self.text}, complete: {self.complete}"
