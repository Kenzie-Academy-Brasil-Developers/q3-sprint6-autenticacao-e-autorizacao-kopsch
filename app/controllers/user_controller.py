from flask import request, jsonify
from http import HTTPStatus
from app.models.user_model import User
from sqlalchemy.exc import IntegrityError
from app.configs.auth import auth
from app.configs.database import db

def create_user():
    try:
        user_data = request.get_json()

        password_to_hash = user_data.pop("password")

        new_user = User(**user_data)

        new_user.password = password_to_hash

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user), HTTPStatus.CREATED
    except KeyError:
        return {"message": "Data missing"}, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {"message": "email already exists"}, HTTPStatus.BAD_REQUEST

def login():
    user_data = request.get_json()
    
    found_user: User = User.query.filter_by(email=user_data["email"]).first()
    
    if not found_user:
        return {"message": 'User not found'}, HTTPStatus.UNAUTHORIZED
    
    if found_user.verify_password(user_data["password"]):
        return {"api_key": found_user.api_key}, HTTPStatus.OK
    else:
        return {"message": "Wrong password"}, HTTPStatus.UNAUTHORIZED
    
@auth.login_required
def get_user():
    if auth.current_user() != 'Not Found':
        return jsonify(auth.current_user()), HTTPStatus.OK
    else:
        return {'error': 'user not found'}, HTTPStatus.NOT_FOUND
  
@auth.login_required  
def put_user():
    user_data = request.get_json()
    user = auth.current_user()
    
    password = user_data.pop('password')
    
    for key, value in user_data.items():
        setattr(user, key, value)
        
    user.password = password
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user), HTTPStatus.OK

@auth.login_required
def delete_user():
    user = auth.current_user()
    
    db.session.delete(user)
    db.session.commit()
    
    return {'message': f"User {user.name} has been deleted"}, HTTPStatus.OK