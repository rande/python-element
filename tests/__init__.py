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

from tornado.httpserver import HTTPRequest
from tornado.web import Application
from ioc.extra.tornado.handler import BaseHandler
from element.plugins.node.jinja import get_dummy_connection

class TestHandler(BaseHandler):
    def finish(self):
        self._finished = True


def get_default_handler():
    return TestHandler(Application(), HTTPRequest("GET", "/", connection=get_dummy_connection()))


class TemplateEngine(object):
    """
    Mock jinja engine ...
    """
    def get_template(self, name):
        return Template(name)

class Template(object):
    def __init__(self, name):
        self.name = name

    def render(self, params):
        return self.name

