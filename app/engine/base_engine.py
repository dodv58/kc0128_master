class BaseEngine:
    def init_app(self, app):
        pass
    def is_installed(self):
        raise NotImplementedError()
    def update_engine(self):
        raise NotImplementedError()
    def running_status(self):
        raise NotImplementedError()
    def start_service(self):
        raise NotImplementedError()
    def stop_service(self):
        raise NotImplementedError()
    def restart_service(self):
        raise NotImplementedError()
    def disconnect(self):
        raise NotImplementedError()