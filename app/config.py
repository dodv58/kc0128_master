class Config(object):
    """
    Common configurations
    """
    # Put any configurations here that are common across all environments
    DEBUG = False
    LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
                'level': 'INFO',
            }
        },
        'loggers': {
            'gunicorn.error': {
                'level': 'INFO',
                'handlers': ['wsgi'],
                'propagate': False,
            },
            'gunicorn.access': {
                'level': 'INFO',
                'handlers': ['wsgi'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    }


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    FLASK_ENV = 'development'
    DEBUG = True
    LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
                'level': 'DEBUG',
            },
            'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'filename': 'logs/app.log',
                'when': 'midnight',
                'interval': 1,
                'level': 'DEBUG',
            },
        },
        'loggers': {
            'gunicorn.error': {
                'level': 'DEBUG',
                'handlers': ['wsgi'],
                'propagate': False,
            },
            'gunicorn.access': {
                'level': 'INFO',
                'handlers': ['wsgi'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }


class ProductionConfig(Config):
    """
    Production configurations
    """
    FLASK_ENV = 'production'


class TestConfig(Config):
    """
    Development configurations
    """
    FLASK_ENV = 'test'
    DEBUG = True
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
}

