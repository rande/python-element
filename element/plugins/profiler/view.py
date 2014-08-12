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

class ProfilerView(object):
    def __init__(self, profiler):
        self.profiler = profiler


    def home(self):
        pass

    def view(self, request_handler, token, **kwargs):

        panel = request_handler.get_argument('panel')

        run = self.profiler.load_run(token)

        return 200, self.profiler.get_template_name(run, panel), {
            'run': run,
            'panel': panel,
            'collector': run.get_metric(panel),
            'templates': self.profiler.get_templates(run),
            'token': token,
            'position': 'bottom',
            'profile': run,
            'is_ajax': request_handler.is_xml_http_request()
        }

    def pyinfo(self, request_handler, token, **kwargs):
        pass

    def wdt(self, request_handler, token, **kwargs):

        run = self.profiler.load_run(token)

        return 200, 'element.plugins.profiler:profiler/toolbar.html', {
            'run': run,
            'token': token,
            'position': 'bottom',
            'profile': run,
            'templates': self.profiler.get_templates(run)
        }

    def export_run(self):
        pass

    def purge_run(self):
        pass

    def import_run(self):
        pass
