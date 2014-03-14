import element.node

class GalleryHandler(element.node.NodeHandler):
    def __init__(self, templating):
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.media:gallery.html'
        }

    def get_name(self):
        return 'Media Gallery'

    def execute(self, request_handler, context):
        medias = context.node.medias()

        params = {
            'context': context,
            'medias':  medias,
            'lines': [
                [x for x in range(len(medias)) if x - 0 == 0 or ((x - 0) % 4 == 0)],
                [x for x in range(len(medias)) if x - 1 == 0 or ((x - 1) % 4 == 0)],
                [x for x in range(len(medias)) if x - 2 == 0 or ((x - 2) % 4 == 0)],
                [x for x in range(len(medias)) if x - 3 == 0 or ((x - 3) % 4 == 0)],
            ],
        }
        
        self.render(request_handler, self.templating, context.settings['template'], params)

class MediaHandler(element.node.NodeHandler):

    def __init__(self, templating):
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.media:media.html'
        }

    def get_name(self):
        return 'Media'

    def execute(self, request_handler, context):

        params = {
            'context': context,
        }

        self.render(request_handler, self.templating, context.settings['template'], params)