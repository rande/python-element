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

import element
import sys
import platform
import os
import inspect, importlib
from datetime import datetime
import resource

class BaseCollector(object):
    def on_request(self, request_handler, run):
        pass

    def on_callback(self, request_handler, run, name, callback, parameters):
        pass

    def on_terminate(self, request_handler, run):
        pass

    def on_response(self, request_handler, run):
        pass

    def get_template(self, run):
        return False

class RequestCollector(BaseCollector):
    def on_request(self, request_handler, run):
        request = request_handler.request

        run.add_metric('request', {
            'method': request.method,
            'uri': request.uri,
            'path': request.path,
            'query': request.query,
            'version': request.version,
            'headers': request.headers,
            'protocol': request.protocol,
            'host': request.host,
            'body': request.body,
            'query_arguments': request.query_arguments,
            'body_arguments': request.body_arguments,
            'cookies': request.cookies.output(),
            'remote_ip': request.remote_ip,

            # this will be set on other events
            'status_code': False,
            'route': False,
            'controller': {
                'class': False,
                'file': False,
                'line': False,
                'method': False
            }
        })

    def get_class_name(self, method):
        # <class 'tests.plugins.profiler.test_collector.NodeHandler'>
        return ("%s" % method.im_class)[8:-2]

    def get_method_name(self, method):
        # <function execute at 0x2a60ed8>
        return ("%s" % method.im_func).split(" ")[1]

    def on_callback(self, request_handler, run, name, callback, parameters):
        run.get_metric('request').update({
            'route': name,
            'controller': {
                'class': self.get_class_name(callback),
                'method': self.get_method_name(callback)
            },
            'route_parameters': parameters
        })

    def on_response(self, request_handler, run):
        run.get_metric('request').update({
            'status_code': int(request_handler.get_status())
        })



    def get_template(self, run):
        return 'element.plugins.profiler:collector/request.html'

class PyInfo(object):
    def __init__(self):
        self._buid = False
        self.system = {}
        self.build()

    def build(self):
        self.build_system()
        self._buid = True

    def get_system(self, name=None):
        if not name:
            return self.system

        return self.system[name]

    def build_system(self):
        """
        from https://github.com/Dreyer/pyinfo/blob/master/pyinfo.py
        """
        system = {
            'path': False,
            'os_path': False,
            'os_version': False,
            'version': False,
            'subversion': False,
            'prefix': False,
            'build_date': platform.python_build()[1],
            'executable': False,
            'compiler': platform.python_compiler(),
            'api_version': False,
            'implementation': platform.python_implementation(),
            'system': platform.system(),
        }

        if platform.dist()[0] != '' and platform.dist()[1] != '':
            system['os_version'] = '%s %s (%s %s)' % ( platform.system(), platform.release(), platform.dist()[0].capitalize(), platform.dist()[1] )
        else:
            system['os_version'] = '%s %s' % ( platform.system(), platform.release() )

        if hasattr( os, 'path' ): system['os_path'] = os.environ['PATH']
        if hasattr( sys, 'version' ): system['version'] = platform.python_version()
        if hasattr( sys, 'subversion' ): system['subversion'] = ', '.join( sys.subversion )
        if hasattr( sys, 'prefix' ): system['prefix'] = sys.prefix
        if hasattr( sys, 'path' ): system['path'] = sys.path
        if hasattr( sys, 'executable' ): system['executable'] = sys.executable
        if hasattr( sys, 'api_version' ): system['api'] = sys.api_version

        self.system = system

class TimeCollector(BaseCollector):
    def on_request(self, request_handler, run):
        run.add_metric('time', {
            'start': datetime.now(),
            'delta': False,
            'delta_format': False,
            'end': False
        })

    def on_terminate(self, request_handler, run):
        now = datetime.now()
        start = run.get_metric('time')['start']
        delta = (now - start).total_seconds() * 1000

        run.get_metric('time').update({
            'end': now,
            'delta': delta,
            'delta_format': "%.2f ms" % delta
        })

    def get_template(self, run):
        return 'element.plugins.profiler:collector/time.html'

class MemoryCollector(BaseCollector):
    def on_request(self, request_handler, run):
        run.add_metric('memory', {
            'start': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'delta': False,
            'delta_format': False,
            'end': False
        })

    def on_terminate(self, request_handler, run):
        now = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        start = run.get_metric('memory')['start']
        delta = now - start

        run.get_metric('memory').update({
            'end': now,
            'delta': delta,
            'delta_format': "%f" % delta
        })

    def get_template(self, run):
        return 'element.plugins.profiler:collector/memory.html'

class ConfigCollector(BaseCollector):
    def __init__(self, container):
        self.container = container

    def on_request(self, request_handler, run):

        info = PyInfo()
        run.add_metric('config', {
            'element_version': element.__version__,
            'app_name': 'element',
            'application_name': 'n/a',
            'application_version': 'n/a',
            'debug': self.container.parameters.get('ioc.debug'),
            'env': self.container.parameters.get('ioc.env'),
            'python': info.get_system(),
            'extensions': self.get_extensions()
        })

    def get_extensions(self):
        extensions = {}
        for extension in self.container.parameters.get('ioc.extensions'):
            extensions[extension] = inspect.getfile(importlib.import_module(extension))

        return extensions

    def get_template(self, run):
        return 'element.plugins.profiler:collector/config.html'