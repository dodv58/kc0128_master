from app.engine.base_engine import BaseEngine
import json, yaml
import os
from app import utils
from .suricatasc.suricatasc import *

import logging
logger = logging.getLogger()

class Suricata(BaseEngine):
    config = None
    commands = None
    sc = None

    def init_app(self, app):
        # config for suricata instance
        with open('%s/engine/suricata/config.yml' % app.root_path) as fp:
            self.config = yaml.load(fp, Loader=yaml.FullLoader)

        for k, v in app.config.items():
            self.config[k] = v

        # read commands from config file
        config_file = "{}/engine/suricata/suricata_{}.conf".format(app.root_path, self.config.get('OS_TYPE') or 'centos')
        with open(config_file) as c:
            self.commands = json.load(c)

        self.sc = self.init_suricatasc()

    def init_suricatasc(self):
        SOCKET_PATH = os.path.join(self.config.get('LOCAL_STATE_DIR'), "suricata-command.socket")
        sc = SuricataSC(SOCKET_PATH)
        try:
            sc.connect()
            print("Connected to socket: %s" % SOCKET_PATH)
            return sc
        except SuricataNetException as err:
            print("Unable to connect to socket %s: %s" % (SOCKET_PATH, err), file=sys.stderr)
            return None
        except SuricataReturnException as err:
            print("Unable to negotiate version with server: %s" % (err), file=sys.stderr)
            return None


    def suri_path(self):
        path = self.commands.get('suriPath')
        if not path:
            return False
        return os.path.exists(path)

    def suri_bin(self):
        command = self.commands.get('suriBin')
        if not command:
            return False
        return_code, out, err = utils.system_execute(command.get('cmd'), command.get('params'))
        if not return_code and 'Suricata version' in out:
            return True
        else:
            return False

    def running_status(self):
        command = self.commands.get('suriRunning')
        if not command:
            return False
        return_code, out, err = utils.system_execute(command.get('cmd'), command.get('params'))
        if not return_code and out.strip().isnumeric():
            logger.info("PID = {}".format(out))
            return True
        else:
            logger.error("Return_code: %s, out: %s, err: %s", return_code, out, err)
            return False

    def start_service(self):
        command = (self.commands.get('suricata') or {}).get('start')
        if not command:
            return False
        return_code, out, err = utils.system_execute(command)
        if return_code:
            logger.error(err)
            return False
        else:
            logger.info(out)
            return True

    def stop_service(self):
        command = (self.commands.get('suricata') or {}).get('stop')
        if not command:
            return False
        return_code, out, err = utils.system_execute(command)
        if return_code:
            logger.error(err)
            return False
        else:
            logger.info(out)
            return True

    def get_iface_list(self):
        (command, arguements) = self.sc.parse_command('iface-list')
        res = self.sc.send_command(command, arguements)
        return res

    def disconnect(self):
        if self.sc:
            self.sc.close()