from app.database import models
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import jwt
import time
import os
logger = logging.getLogger()

def register_user(data):
    try:
        user = models.User.find_by_name(name=data['username'])
        if user:
            return {'error': 'User already exists!!!'}, 501
        models.User(name=data['username'], password=generate_password_hash(data['password'])).save_to_db()
    except Exception as e:
        logger.error(e)
        return {'error': 'An error occurred saving the user to the database'}, 500
    return {'message': 'User registered successfully'}, 201

def login(data):
    user = models.User.find_by_name(data['username'])
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({
            'exp': int(time.time()) + int(os.getenv('TOKEN_EXPIRE_TIME')),
            'username': user.name
        }, os.getenv('JWT_SECRET'), algorithm='HS256')
        return {'token': token.decode('utf-8')}, True
    return {'error': 'User or password are incorrect'}, False

def verify_token(token):
    if not token:
        return 'No token found', False
    try:
        paypoad = jwt.decode(token, os.getenv('JWT_SECRET'), algorithm='HS256')
        return paypoad.get('username'), True
    except jwt.ExpiredSignatureError:
        return "Signature has expired", False
    except Exception as e:
        logger.error(e)
        return 'Token incorrect', False
