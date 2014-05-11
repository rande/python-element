from ioc.helper import deepcopy

class SeoPage(object):
    def __init__(self, title_pattern="%s", metas=None, keywords=None):
        self.title_pattern = title_pattern
        self.metas = metas or {}
        self.keywords = keywords or []

class SeoListener(object):
    def __init__(self, seo_page):
        self.seo_page = seo_page

    def add_seo(self, event):
        """
        Add SEO information into the current node
        """
        context = event.get('context')

        if context.node.type == 'seo.headers':
            return

        if 'seo' not in context.settings:
            context.settings['seo'] = {}

        self.configure_title(context)
        self.configure_metas(context)

    def configure_title(self, context):
        title = None

        if 'title' in context.settings['seo']:
            title = context.settings['seo']['title']
        else:
            for field in ['title', 'name']:
                title = context[field]

                if title:
                    break

        if title:
            context.settings['seo']['title'] = self.seo_page.title_pattern % title

    def configure_metas(self, context):

        if 'metas' not in context.settings['seo']:
            context.settings['seo']['metas'] = {}

        for pname, pmetas in deepcopy(self.seo_page.metas).iteritems():
            if pname not in context.settings['seo']['metas']:
                context.settings['seo']['metas'][pname] = pmetas

            else:  # merge values
                for mname, mvalue in pmetas.iteritems():

                    # print "pname:", pname
                    # print "mname:", mname
                    # print "data:", context.settings['seo']['metas'][pname]

                    if mname not in context.settings['seo']['metas'][pname]:
                        context.settings['seo']['metas'][pname][mname] = mvalue

