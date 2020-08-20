from flask import Flask, request
import os, orjson, logging, signal
from logging.config import dictConfig
from .config import app_config
import yaml
from .utils import build_config_from_env

DEFAULT_CONFIG_NAME = os.getenv('ENV', 'production')

def handle_sigterm(signum, frame):
    logging.info('Gracefully exit')
    logging.info('System exit')
    raise SystemExit

def create_app(config_name=DEFAULT_CONFIG_NAME):
    global db
    app = Flask(__name__, instance_relative_config=True)

    # ensure the logs folder exists
    os.makedirs('./logs', exist_ok=True)

    # load common & default config values
    app.config.from_object(app_config[config_name])
    with open('%s/config.yml' % app.root_path) as fp:
        app.config.from_mapping(yaml.load(fp, Loader=yaml.FullLoader))

    # Override configs by ENV variables
    app.config.from_mapping(build_config_from_env(app))

    # init logging
    dictConfig(app.config.get('LOGGING'))

    # init database
    from . import database
    db = database.init_app(app)

    # init authentication
    from . import authentication
    authentication.init_app(app)

    from .authentication.auth_middleware import Auth
    app.wsgi_app = Auth(app.wsgi_app)

    # /ping
    @app.route('/healthz')
    def ping():
        print(request.environ['username'])
        return app.response_class(
            orjson.dumps({'message': 'ok'}),
            mimetype=app.config['JSONIFY_MIMETYPE'],
        ), 200

    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)

    return app