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

from element.node import NodeHandler
from tornado.process import Subprocess
from tornado.concurrent import Future
import wtforms, wtforms.validators

import uuid

PDF_SETTINGS = {
    'default': 'wkhtmltopdf --quiet %s %s',
    'print': 'wkhtmltopdf -T 0 -R 0 -B 0 -L 0 --dpi 300 --print-media-type --quiet %s %s',
    'shower': 'wkhtmltopdf -T 0 -R 0 -B 0 -L 0 --page-width 27.093333333cm --page-height 16.933333333cm --dpi 300 --print-media-type --quiet %s %s',
}

class GeneratePdfExecutor(object):
    def __init__(self, data_path, request_handler, pdf, logger=None):
        self.data_path = data_path
        self.logger = logger
        self.request_handler = request_handler
        self.pdf = pdf

    def run(self):
        self.output = '%s/%s.%s' % (self.data_path, self.pdf.id, self.pdf.format)

        if self.logger:
            self.logger.debug("GeneratePdfExecutor: Start generating %s from %s (pdf.id:%s)" % (self.output, self.pdf.url, self.pdf.id))

        args = PDF_SETTINGS[self.pdf.setting_name] % (self.pdf.url, self.output)

        if self.logger:
            self.logger.debug("GeneratePdfExecutor: executing: %s" % args)

        self.p = Subprocess(args.split(" "), stdout=Subprocess.STREAM, stderr=Subprocess.STREAM)
        self.p.set_exit_callback(self.send_end)

        self.p.stdout.read_until("\n", self.send_stdout)
        self.p.stderr.read_until("\n", self.send_stderr)

        self.f = Future()

        return self.f

    def send_stdout(self, data):
        if self.logger:
            self.logger.debug("GeneratePdfExecutor: stdout: %s" % data.strip())

        self.p.stdout.read_until("\n", self.send_stdout)

    def send_stderr(self, data):
        if self.logger:
            self.logger.error("GeneratePdfExecutor: stderr: %s" % data.strip())

        self.p.stderr.read_until("\n", self.send_stderr)

    def send_end(self, status_code):
        if self.logger:
            self.logger.debug("GeneratePdfExecutor: status_code: %s" % status_code)

        self.request_handler.send_file(self.output)

        self.f.set_result(True)

class GeneratePdfForm(wtforms.Form):
    url = wtforms.TextField('url', validators=[wtforms.validators.DataRequired(), wtforms.validators.URL()])
    setting_name = wtforms.SelectField('format',
        option_widget=wtforms.widgets.Select,
        choices=[('default', 'Default'), ('shower', 'Shwr.me'), ('print', 'Print')],
        validators=[wtforms.validators.AnyOf(['default', 'print', 'shower']), wtforms.validators.DataRequired()]
    )

class GeneratePdf(object):
    def __init__(self, url=None, format="pdf", options=None):
        self.url = url
        self.format = format
        self.setting_name = 'default'
        self.options = options or {}
        self.id = uuid.uuid4()

class GeneratePdfView(object):
    def __init__(self, data_path, logger=None):
        self.data_path = data_path
        self.logger = logger

    def execute(self, request_handler, context, **kwargs):
        pdf = GeneratePdf()
        form = GeneratePdfForm(request_handler.get_form_data(), pdf)

        if request_handler.get_argument('url', default=None) and form.validate():
            form.populate_obj(pdf)

            return GeneratePdfExecutor(self.data_path, request_handler, pdf, logger=self.logger).run()

        return 200, 'element.plugins.wkhtmltopdf:pdf.html', {
            'form': form,
            'context': context
        }