
class StaticView(object):
    def __init__(self, locator):
        self.locator = locator

    def execute(self, request_handler, module, filename):
        file = self.locator.locate("%s:static/%s" % (module, filename))

        request_handler.send_file(file)