from ioc.component import Extension
from ioc.loader import YamlLoader
import os

class Extension(Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = YamlLoader()
        loader.load("%s/resources/config/services_node.yml" % path, container_builder)

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

        logger = container.get('element.logger')

        def wrapper(function):
            return lambda node, *args, **kwargs: function(node, *args, **kwargs)

        for type, meta in collection.metas.iteritems():
            for name, method in meta.methods.iteritems():
                logger.debug("element.plugins.node.post_build: attach %s to %s with %s" % (name, type, method))
                setattr(meta.klass, name, wrapper(method))
