import mimetypes

class StaticView(object):
    def __init__(self, locator):
        self.locator = locator

    def execute(self, request_handler, module, filename):
        file = self.locator.locate("%s:static/%s" % (module, filename))

        mime_type, encoding = mimetypes.guess_type(file)

        if mime_type:
            request_handler.set_header('Content-Type', mime_type)

        fp = open(file, 'r')
        request_handler.write(fp.read())

        fp.close()
