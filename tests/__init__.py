# vim: set fileencoding=utf-8 :

from tornado.httpserver import HTTPRequest
from tornado.web import Application
from ioc.extra.tornado.handler import BaseHandler


class TestHandler(BaseHandler):
    def finish(self):
        self._finished = True


def get_default_handler():
    return TestHandler(Application(), HTTPRequest("GET", "/"))


class TemplateEngine(object):
    """
    Mock jinja engine ...
    """
    def get_template(self, name):
        return Template(name)

class Template(object):
    def __init__(self, name):
        self.name = name

    def render(self, params):
        return self.name

