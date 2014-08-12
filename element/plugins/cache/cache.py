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

class CacheControl(object):
    """
    This class attach cache header to the request matching the pattern
    """

    def __init__(self, rules=None):
        self.rules = rules or []

    def cache_control(self, event):
        request_handler = event.get('request_handler')

        if request_handler.request.method in ["GET", "HEAD"]:
            values = self.find_values(request_handler.request.path)
        else:
            values = self.get_default()

        for name, value in values.iteritems():
            request_handler.set_header(name, ", ".join(value))

    def find_values(self, path):
        for rule, values in self.rules:
            if rule.match(path):
                return values

        return self.get_default()

    def get_default(self):
        return {
            'Cache-Control': ['private', 'must-revalidate']
        }