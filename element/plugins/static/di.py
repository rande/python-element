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

import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/handler_static.yml" % path, container_builder)

        container_builder.parameters.set('element.static.mapping', {
            'jpg': 'image/jpeg',
            'JPG': 'image/jpeg',
            'png': 'image/png',
            'PNG': 'image/png',
            'gif': 'image/gif',
            'GIF': 'image/gif',
            'js': 'application/x-javascript; charset=utf-8',
            'css': 'text/css; charset=utf-8',
            'json': 'application/json; charset=utf-8',
            'txt': 'text/plain; charset=utf-8',
            'xml': 'text/xml; charset=utf-8',
            'rss': 'application/rss+xml; charset=utf-8',
            'ico': 'image/x-icon',
            'html': 'text/html'
        })

        container_builder.get('element.plugins.static').arguments[2] = config.get_all('temp_dir', '%project.root_folder%/data/element.plugins.static')

    def post_build(self, container_builder, container):

        router = container.get('ioc.extra.tornado.router')

        router.add('element.static', '/element/static/<string:module>/<path:filename>', **{
            'methods': ['GET'],
            'view_func': container.get('element.plugins.static.view').execute
        })
