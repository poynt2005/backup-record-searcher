from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    def load_config(self):
        s = self.cfg.set
        s('bind', '0.0.0.0:8586')
        s('timeout', 300)
        s('accesslog', '/server_log/access.log')
        s('errorlog', '/server_log/error.log')
        s('loglevel', 'debug')

    def load(self):
        from app import app
        return app


if __name__ == '__main__':
    Application().run()
