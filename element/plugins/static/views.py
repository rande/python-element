import flask
from flask.views import MethodView

class StaticView(MethodView):
    def __init__(self, locator):
        self.locator = locator

    def get(self, module, path):

        file = self.locator.locate("%s:static/%s" % (module, path))

        return flask.send_file(file)