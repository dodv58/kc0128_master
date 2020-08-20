from . import blueprint
from flask import request
from app.utils import json_response
from . import auth
import logging
logger = logging.getLogger()

@blueprint.route('/register', methods=['POST'])
def register():
    res, code = auth.register_user(request.json)
    return json_response(data=res, code=code)

@blueprint.route('/login', methods=['POST'])
def login():
    res, code = auth.login(request.json)
    return json_response(data=res, code= 200 if code else 401)
@blueprint.route('/logout')
def logout():
    pass