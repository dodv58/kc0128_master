from flask import jsonify
import os
import subprocess


def json_response(code=200, data=None, description=None, **kwargs):
    code = int(code)
    response = {
        'data': data if data and (isinstance(data, dict) or isinstance(data, list)) else {},
        'status': {
            'code': code,
            'description': description if description and isinstance(description, str) else '',
        },
    }

    if kwargs:
        for k, v in kwargs.items():
            response[k] = v

    return jsonify(response), code

def build_config_from_env(app):
    env_config = {}

    for k, v in os.environ.items():
        if k in app.config:
            current_value = app.config.get(k)
            try:
                if isinstance(current_value, bool):
                    env_config[k] = True if v.lower() in ['true', 'yes', '1', 'y'] else False
                elif isinstance(current_value, float):
                    env_config[k] = float(v)
                elif isinstance(current_value, int):
                    env_config[k] = int(v)
                else:
                    env_config[k] = v
            except ValueError:
                pass
        else:
            env_config[k] = v

    return env_config
