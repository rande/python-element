import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/handler_node.yml" % path, container_builder)
        loader.load("%s/resources/config/jinja.yml" % path, container_builder)
        loader.load("%s/resources/config/listener_standardize.yml" % path, container_builder)