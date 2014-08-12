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

import uuid
import os
import hashlib
from datetime import datetime
import pickle
try:
    # included in standard lib from Python 2.7
    from collections import OrderedDict
except ImportError:
    # try importing the backported drop-in replacement
    # it's available on PyPI
    from ordereddict import OrderedDict

class Run(object):
    def __init__(self, id=None):
        self.data = {}
        self.metrics = {}
        self.time = datetime.today()
        self.ip = False
        self.url = False
        self.method = False

        if not id:
            h = hashlib.sha256()
            h.update("%s" % uuid.uuid4())
            id = h.hexdigest()[0:8]

        self.id = id

    def add_data(self, name, value):
        self.data[name] = value

    def get_data(self, name):
        return self.data[name]

    def add_metric(self, name, value):
        self.metrics[name] = value

    def get_metric(self, name):
        return self.metrics[name]

class ProfilerListener(object):
    def __init__(self, enabled, profiler, templating):
        self.enabled = enabled
        self.profiler = profiler
        self.templating = templating

        # to do: move this to configuration
        import re
        self.ignore_patterns = [
            re.compile("/profiler"),
            re.compile("/static"),
            re.compile("/element/static"),
            re.compile(".*(png|gif|jpg|css)"),
        ]

    def on_request(self, event):
        request_handler = event.get('request_handler')

        if not self.enabled:
            return

        for re in self.ignore_patterns:
            if re.match(request_handler.request.path):
                return

        run = self.profiler.create_run()
        run.url = request_handler.request.uri
        run.ip = request_handler.request.remote_ip
        run.method = request_handler.request.method

        request_handler = event.get('request_handler')
        request_handler.add_header('X-Profiler-Id', "%s" % run.id)
        request_handler.run = run

        for name, collector in self.profiler.collectors.iteritems():
            collector.on_request(request_handler, run)

    def on_callback(self, event):
        request_handler = event.get('request_handler')

        if not hasattr(request_handler, 'run'):
            return

        for name, collector in self.profiler.collectors.iteritems():
            collector.on_callback(request_handler, request_handler.run, event.get('name'), event.get('callback'), event.get('parameters'))

    def on_response(self, event):
        """
        The toolbar is only injected for text/html content, done otherwise
        The X-Profiler-Id is still available in the response header
        """
        request_handler = event.get('request_handler')

        if not hasattr(request_handler, 'run'):
            return

        content_type = request_handler.get_header('Content-Type')

        if len(content_type) < 9 or content_type[0:9] != 'text/html':
            return

        if request_handler.request.headers.get('Surrogate-Capability'):
            return

        if request_handler.get_query_argument('_element', default=False) == 'no-debug':
            return

        ## inject the toolbar to the response
        content = self.templating.get_template('element.plugins.profiler:profiler/toolbar_js.html').render({
            'token': str(request_handler.run.id)
        })

        chunk = request_handler.get_chunk_buffer().decode('utf-8')
        request_handler.reset_chunk_buffer()

        k = chunk.rfind('</body>')

        request_handler.write(chunk[:k])
        request_handler.write(content)
        request_handler.write(chunk[k:])

        for name, collector in self.profiler.collectors.iteritems():
            collector.on_response(request_handler, request_handler.run)

    def on_terminate(self, event):
        request_handler = event.get('request_handler')

        if not hasattr(request_handler, 'run'):
            return

        for name, collector in self.profiler.collectors.iteritems():
            collector.on_terminate(request_handler, request_handler.run)

        self.profiler.store_run(request_handler.run)

class Profiler(object):
    def __init__(self, output_path, templating):
        self.output_path = output_path
        self.templating = templating
        self.collectors = OrderedDict()

    def add_collector(self, name, collector):
        self.collectors[name] = collector

    def create_run(self):
        run = Run()

        path = "%s/%s" % (self.output_path, run.id)
        os.makedirs(path)

        return run

    def load_run(self, id):
        path = "%s/%s/metric.bin" % (self.output_path, id)

        return pickle.load(open(path, "rb"))

    def store_run(self, run):
        path = "%s/%s/metric.bin" % (self.output_path, run.id)

        data = run.data
        run.data = {}

        pickle.dump(run, open(path, "wb"))

        run.data = data

    def get_template_name(self, run, name):
        return self.collectors[name].get_template(run)

    def get_templates(self, run):
        templates = []
        for name, collector in self.collectors.iteritems():
            template = collector.get_template(run)

            if template:
                templates.append((name, self.templating.get_template(template)))

        return templates