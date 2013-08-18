import ioc
import os

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/security.yml" % path, container_builder)

        self.configure_providers(config.get_dict('providers'), container_builder)

    def configure_providers(self, config, container_builder):
        self.configure_inmemory_provider(config.get_dict('in_memory'), container_builder)


    def configure_inmemory_provider(self, config, container_builder):
        container_builder.parameters.set('element.plugins.security.in_memory_users', config.get('users', []))