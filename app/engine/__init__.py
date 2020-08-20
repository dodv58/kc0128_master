from .suricata.suricata import Suricata

def init_engine(app):
    suri = Suricata()
    suri.init_app(app)
    return suri