from flask import request
from app.utils import json_response
from app import _engine
from . import (
    blueprint
)

@blueprint.route('/running-status', methods=['GET'])
def get_engine_running_status():
    status = _engine.running_status()
    return json_response(data={
        'status': status
    })

@blueprint.route('/start', methods=['POST'])
def start_engine():
    res = _engine.start_service()
    return json_response(data={
        'status': res
    })

@blueprint.route('/stop', methods=['POST'])
def stop_engine():
    res = _engine.stop_service()
    return json_response(data={
        'status': res
    })

@blueprint.route('/iface-list', methods=['GET'])
def get_iface_list():
    res = _engine.get_iface_list()
    return json_response(data={
        'status': res
    })
