import ioc
import os, re

class Extension(ioc.component.Extension):
    def load(self, config, container_builder):
        path = os.path.dirname(os.path.abspath(__file__))

        loader = ioc.loader.YamlLoader()
        loader.load("%s/resources/config/listener_cache.yml" % path, container_builder)

        rules = []

        for rule in config.get('cache_control', []):
            path = rule['path']

            del(rule['path'])

            rules.append((re.compile(path), rule))

        container_builder.parameters.set('element.cache.rules', rules)
