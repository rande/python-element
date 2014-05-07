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
        node = event.get('node')

        if 'seo' not in node.data:
            node.data['seo'] = {}

        node.data['seo']['title'] = self.seo_page.title_pattern % node.title

        self.replace_if_empty(node.data['seo'], 'keywords', self.seo_page.keywords)
        self.replace_if_empty(node.data['seo'], 'metas', self.seo_page.metas)

    def replace_if_empty(self, dict, key, value):
        if key in dict and not dict[key]:
            return

        dict[key] = value
