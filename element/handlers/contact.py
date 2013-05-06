import element.handlers
import element.node

class Contact(object):
    def __init__(self, name=None, email=None, message=None):
        self.name = name
        self.email = email
        self.message = message

class ContactHandler(element.handlers.NodeHandler):
    def __init__(self, email):
        self.email = email

    def get_defaults(self, node):
        return {
            'template': 'handlers/contact/form.html'
        }

    def execute(self, context, flask):
        params = {
            'sent': False,
            'context': context
        }

        if flask.request.method == "POST":
            contact = Contact(
                flask.request.form['name'],
                flask.request.form['email'],
                flask.request.form['message'],
            )

            # send an email
            #  => RTFM (when online of cour)
            return flask.redirect(flask.request.path + '?confirmation')

        if 'confirmation' in flask.request.args:
            params['sent'] = True

        return flask.make_response(flask.render_template(context.settings['template'], **params))
