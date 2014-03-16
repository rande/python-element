# vim: set fileencoding=utf-8 :

from tornado.httpserver import HTTPRequest
from tornado.web import Application
from ioc.extra.tornado.handler import BaseHandler


class TestHandler(BaseHandler):
    def finish(self):
        self._finished = True


def get_default_handler():
    return TestHandler(Application(), HTTPRequest("GET", "/"))


class Templating(object):
    def render(self, template, **kwargs):
        return template