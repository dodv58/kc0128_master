from werkzeug.wrappers import Request, Response, ResponseStream
from .auth import verify_token

class Auth():
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ.get('REQUEST_URI').startswith('/auth'):
            return self.app(environ, start_response)

        user, status = verify_token(environ.get('HTTP_USER_TOKEN'))

        if status:
            environ['username'] = user
            return self.app(environ, start_response)
        else:
            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)