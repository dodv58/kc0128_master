from flask import Blueprint

MODULE_NAME = 'engine'
blueprint = Blueprint(MODULE_NAME, __name__)

from . import apis

def init_app(app, url_prefix=None):
    app.register_blueprint(blueprint=blueprint, url_prefix=(url_prefix if url_prefix else '/' + MODULE_NAME))