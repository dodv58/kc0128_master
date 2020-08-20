from flask_sqlalchemy import SQLAlchemy

def init_app(app):
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        return None
    _db = SQLAlchemy(app)
    return _db
