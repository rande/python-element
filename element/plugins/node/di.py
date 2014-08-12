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

from ioc.component import Extension
from ioc.loader import YamlLoader
import os

class Extension(Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = YamlLoader()
        loader.load("%s/resources/config/services_node.yml" % path, container_builder)

        definition = container_builder.get  ('element.plugins.node.jinja2.master')
        definition.arguments[4] = config.get('render_type', 'esi')

    def post_build(self, container_builder, container):
        """
        The build is over, register services-as-methods
        """
        collection = container.get('element.plugins.node.mapper.meta_collection')

        container.get('ioc.extra.event_dispatcher').dispatch('node.mapper.pre_initialize', {
            'meta_collection': collection
        })

        container.get('ioc.extra.event_dispatcher').dispatch('node.mapper.post_initialize', {
            'meta_collection': collection
        })

        logger = container.get('logger')

        def wrapper(function):
            return lambda node, *args, **kwargs: function(node, *args, **kwargs)

        for type, meta in collection.metas.iteritems():
            for name, method in meta.methods.iteritems():
                logger.debug("element.plugins.node.post_build: attach %s to %s with %s" % (name, type, method))
                setattr(meta.klass, name, wrapper(method))
