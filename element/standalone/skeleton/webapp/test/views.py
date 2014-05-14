__author__ = 'rande'

from element.node import NodeHandler
from werkzeug.routing import NotFound, RequestRedirect

class ErrorView(NodeHandler):
    def __init__(self, templating):
        self.templating = templating

    def execute(self, request_handler, error, **kwargs):
        if error == 404:
            raise NotFound()

        if error == 301:
            raise RequestRedirect('/')

        raise Exception()