import element.node

from flask.ext.wtf import Form
import wtforms, wtforms.validators


class ContactForm(Form):
    name = wtforms.TextField('name', validators=[wtforms.validators.DataRequired()])
    email = wtforms.TextField('email', validators=[wtforms.validators.Email(), wtforms.validators.DataRequired()])
    message = wtforms.TextAreaField('message', validators=[wtforms.validators.DataRequired()])


class Contact(object):
    def __init__(self, name=None, email=None, message=None):
        self.name = name
        self.email = email
        self.message = message

class ContactHandler(element.node.NodeHandler):
    def __init__(self, email, mailer):
        self.email = email
        self.mailer = mailer

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.contact:form.html'
        }

    def get_name(self):
        return 'Contact'

    def execute(self, context, flask):

        contact = Contact()
        form = ContactForm(obj=contact)

        params = {
            'sent': False,
            'context': context,
            'form': form
        }

        if form.validate_on_submit():

            form.populate_obj(contact)

            message = "Message sent from %s (%s)\n\n%s\n\n-- End message\n\n" % (
                contact.name, contact.email, contact.message
            )

            mail = self.mailer.create(
                To=context.node.email['to'],
                From=context.node.email['from'],
                Subject=context.node.email['subject'], 
                Body=message
            )

            self.mailer.send(mail)

            return flask.redirect(flask.request.path + '?confirmation')

        if 'confirmation' in flask.request.args:
            params['sent'] = True

        return flask.make_response(flask.render_template(context.settings['template'], **params))
