from flask import request, jsonify
from http import HTTPStatus
from app.models.user_model import User
from sqlalchemy.exc import IntegrityError
from app.configs.database import db
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)

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
        return {"message": 'User not found'}, HTTPStatus.NOT_FOUND
    
    if not found_user.verify_password(user_data["password"]):
        return {"message": "Wrong password"}, HTTPStatus.UNAUTHORIZED

    token = create_access_token(found_user)
    
    return {'access_token': token}, HTTPStatus.OK
    
@jwt_required()
def get_user():
    user = get_jwt_identity()
    
    return jsonify(user), HTTPStatus.OK
  
@jwt_required()  
def put_user():
    user_data = request.get_json()
    user = get_jwt_identity()
    
    password = user_data.pop('password')
    
    for key, value in user_data.items():
        setattr(user, key, value)
        
    user.password = password
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user), HTTPStatus.OK

@jwt_required()
def delete_user():
    user = get_jwt_identity()
    
    db.session.delete(user)
    db.session.commit()
    
    return {'message': f"User {user.name} has been deleted"}, HTTPStatus.OK