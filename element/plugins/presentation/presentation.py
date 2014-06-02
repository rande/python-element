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
            }

        return {}

    def execute(self, request_handler, context):
        self.render(request_handler, self.templating, context.settings['template'], {
            'context': context,
        })
