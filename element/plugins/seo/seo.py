import element.node
from ioc.helper import deepcopy

class SeoPage(object):
    def __init__(self, title_pattern="%s", metas=None, keywords=None):
        self.title_pattern = title_pattern
        self.metas = metas or {}
        self.keywords = keywords or []

class SeoListener(object):
    def __init__(self, seo_page):
        self.seo_page = seo_page

    def listener(self, event):
        """
        listen to element.seo.headers event and return a node with seo information only
        subject should be a NodeContext object
        """
        if not event.has('subject'):
            return

        node = element.node.Node('seo://%s' % event.get('subject').id, {
            'type': 'seo.headers',
            'seo': self.build_seo(event.get('subject')),
        })

        event.set('node', node)

    def build_seo(self, context):
        """
        build the seo information from the provide context
        """
        seo = {
            'title': None,
            'metas': {}
        }

        self.configure_title(context, seo)
        self.configure_metas(context, seo)

        return seo

    def get_title(self, title):
        return self.seo_page.title_pattern % title

    def configure_title(self, context, seo):
        if 'seo' in context.settings and 'title' in context.settings['seo']:
            seo['title'] = self.get_title(context.settings['seo']['title'])

            return

        for field in ['title', 'name']:
            if context[field]:
                seo['title'] = self.get_title(context[field])
                return

        # no title defined!
        seo['title'] = self.get_title(u"\u2605")

    def configure_metas(self, context, seo):
        if 'seo' not in context.settings or 'metas' not in context.settings['seo']:
            seo['metas'] = deepcopy(self.seo_page.metas)

            return

        if 'metas' in context.settings['seo']:
            seo['metas'] = deepcopy(context.settings['seo']['metas'])

        for pname, pmetas in deepcopy(self.seo_page.metas).iteritems():
            if pname not in seo['metas']:
                seo['metas'][pname] = pmetas
                continue

            # merge values
            for mname, mvalue in pmetas.iteritems():
                if mname not in seo['metas'][pname]:
                    seo['metas'][pname][mname] = mvalue
                    

class SeoHandler(element.node.NodeHandler):
    def __init__(self, templating):
        self.templating = templating

    def get_defaults(self, node):
        return {
            'template': 'element.plugins.seo:headers.html'
        }

    def get_name(self):
        return 'Seo'

    def execute(self, request_handler, context):
        return self.render(request_handler, self.templating, context.settings['template'], {
            'context': context,
            'seo': context.seo
        })
