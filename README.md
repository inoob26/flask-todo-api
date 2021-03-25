# Flask User & Todo API

Stack:
- Flask 
- SQLAlchemy (SQLite as DB)

User - model
```
{
    'id': int, 
    'username': str,
    'password': hash,
    'admin_role': bool
}
```

Todo - model
```
{
    'id': int,
    'text': str,
    'complete': bool,
    'user_id': int
}
```

##  Routes:
```
api/v1/login                  # GET
api/v1/user                   # GET, POST
api/v1/user/<int:user_id>     # PUT, DELETE
api/v1/todo                   # GET, POST
api/v1/todo/<int:todo_id>     # PUT, DELETE
```

## Dependency
Install dependecy from `requirements.txt` 
```
pip install -r requirements.txt
```

## Running

First of all you need set environment variables
### Linux \ MacOS
```
export SECRET_KEY='super-secret-key'        # CHANGE IT!
export JWT_SECRET_KEY='super-secret-key2'   # CHANGE IT!

export FLASK_APP=flask-todo-api
export FLASK_ENV=development                # Change it for your case
export FLASK_CONFIG=development             # Change it for your case
```

### Windows
```
set SECRET_KEY='super-secret-key'        # CHANGE IT!
set JWT_SECRET_KEY='super-secret-key2'   # CHANGE IT!

set FLASK_APP=flask-todo-api
set FLASK_ENV=development                # Change it for your case
set FLASK_CONFIG=development             # Change it for your case
```

Run application
```
flask run
```

### Config lists
```
development
testing
production
```
more info see in `config.py`

## HTTP Requests
Before send requests add User to database using `flask shell` consonle

```
flask shell 

>>> user = User(username='<USERNAME>', password='<PASSWORD>', admin_role=<True/False>)
>>> db.session.add(user)
>>> db.session.commit()
>>> exit()

for example
>>> admin = User(username='administrator', password='pass12A@', admin_role=True)
>>> db.session.add(admin)
>>> db.session.commit()
```

## Swagger-ui access
```
http://127.0.0.1:5000/swagger/
```
If you need you can change route in `config.py ` variable `SWAGGER_URL`

## Testing

Set environment variables

### Linux \ MacOS
```
export SECRET_KEY='super-secret-key'        # CHANGE IT!
export JWT_SECRET_KEY='super-secret-key2'   # CHANGE IT!

export FLASK_APP=flask-todo-api
export FLASK_CONFIG=testing                 # Change it for your case
```

### Windows
```
set SECRET_KEY='super-secret-key'        # CHANGE IT!
set JWT_SECRET_KEY='super-secret-key2'   # CHANGE IT!

set FLASK_APP=flask-todo-api
set FLASK_CONFIG=testing                 # Change it for your case
```

Run unit tests
```
pytest -vv
```

