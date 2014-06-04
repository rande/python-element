import element.node

class PresentationHandler(element.node.NodeHandler):
    def __init__(self, templating, formatter):
        self.templating = templating
        self.formatter = formatter

    def get_name(self):
        return 'Presentation'

    def get_defaults(self, node):

        if node.type == 'presentation.shower':
            return {
                'theme':         'ribbon',
                'base_template': 'element.plugins.presentation:shower_base.html',
                'template':      'element.plugins.presentation:shower_node.html',
                'abstract':      False
            }

        if node.type == 'presentation.slideshare':

            width = node.width or 597
            height = 486

            if not node.height:
                height = (width * 3) / 4

            return {
                'template': 'element.plugins.presentation:slideshare.html',
                'width': width,
                'height': height,
                'abstract': False
            }

        return {}

    def execute(self, request_handler, context):
        self.render(request_handler, self.templating, context.settings['template'], {
            'context': context,
        })
