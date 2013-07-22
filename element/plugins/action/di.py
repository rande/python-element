import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/handler_action.yml" % path, container_builder)
        loader.load("%s/resources/config/handler_redirect.yml" % path, container_builder)

        # To do: add this as a configuration option
        loader.load("%s/resources/config/listener_default_index.yml" % path, container_builder)
        loader.load("%s/resources/config/listener_actions.yml" % path, container_builder)