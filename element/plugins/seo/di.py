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
        loader.load("%s/resources/config/seo.yml" % path, container_builder)

        container_builder.parameters.set('element.seo.page.title_pattern', config.get_all('title_pattern', 'Python Element : %s'))
        container_builder.parameters.set('element.seo.page.metas', config.get_all('metas', {}))
        container_builder.parameters.set('element.seo.page.keywords', config.get_all('keywords', ['python', 'elements']))
