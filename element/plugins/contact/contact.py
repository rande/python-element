#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import element.node
from ioc.extra.tornado.router import TornadoMultiDict

import wtforms, wtforms.validators

class ContactForm(wtforms.Form):
    name = wtforms.TextField('name', validators=[wtforms.validators.DataRequired()])
    email = wtforms.TextField('email', validators=[wtforms.validators.Email(), wtforms.validators.DataRequired()])
    message = wtforms.TextAreaField('message', validators=[wtforms.validators.DataRequired()])


class Contact(object):
    def __init__(self, name=None, email=None, message=None):
        self.name = name
        self.email = email
        self.message = message

class ContactHandler(element.node.NodeHandler):
    def __init__(self, templating, email, mailer):
        self.templating = templating
        self.email = email
        self.mailer = mailer

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.contact:form.html'
        }

    def get_name(self):
        return 'Contact'

    def execute(self, request_handler, context):

        contact = Contact()
        form = ContactForm(request_handler.get_form_data(), contact)

        params = {
            'sent': False,
            'context': context,
            'form': form
        }

        if request_handler.request.method == 'POST' and form.validate():

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

            return request_handler.redirect(request_handler.request.path + '?confirmation')

        if 'confirmation' in request_handler.request.arguments:
            params['sent'] = True

        self.render(request_handler, self.templating, context.settings['template'], params)