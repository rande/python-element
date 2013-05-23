class ActionHandler(object):
    def __init__(self, container):
        self.container = container
        
    def get_defaults(self, node):
        return {
            'template': 'element:handlers/action/index.html'
        }

    def execute(self, context, flask):
        service = self.container.get(context.node.serviceId)

        context.settings['flask'] = flask

        result = getattr(service, context.node.method)(context, **(context.node.kwargs or {}))

        # the service return a response nothing to do ...
        if isinstance(result, flask.Response): 
            return result

        if isinstance(result, tuple):
            template, params = result
            return flask.make_response(flask.render_template(template, **params))

        return flask.make_response(flask.render_template(context.settings['template'], **{
            'context': context,
            'content': result
        }))

class RedirectHandler(object):
    def __init__(self, base_url):
        self.base_url = base_url

        if self.base_url[-1] == '/':
             self.base_url = self.base_url[:-1]

    def get_defaults(self, node):
        return {}

    def execute(self, context, flask):
        if 'http://' == context.node.redirect[0:7] or 'https://' == context.node.redirect[0:8]:
            return flask.redirect(context.node.redirect)

        if context.node.redirect[0] == '/': # absolute uri
            return flask.redirect("%s%s" % (self.base_url, context.node.redirect))

        return flask.redirect("%s/%s/%s" % (self.base_url, context.node.id, context.node.redirect))
