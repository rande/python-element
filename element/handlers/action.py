import flask

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

        result = getattr(service, context.node.method)(context, **context.node.kwargs)

        # the service return a response nothing to do ...
        if isinstance(result, flask.Response): 
            return result

        if isinstance(result, tuple):
            template, params = result
            return flask.make_response(flask.render_template(template, **params))

        response = flask.make_response(flask.render_template(context.settings['template'], **{
            'context': context,
            'content': result
        }))

        return response

class RedirectHandler(object):
    def get_defaults(self, node):
        return {}

    def execute(self, context, flask):
        redirect = context.node.redirect

        if redirect[0:1] != '/':
            redirect = "%s/%s" % (context.node.id, redirect)

        return flask.redirect(redirect)
