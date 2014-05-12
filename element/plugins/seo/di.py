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
