import os
from app import create_app

config_name = os.getenv('ENV', 'production')
app = create_app(config_name)

print('Running app in configuration %s' % config_name)


if __name__ == '__main__':
    app.run()