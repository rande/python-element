import os

class FsManager(object):
    """
    This class handle loading of definition from the Filesystem
    """
    def __init__(self, path, manager):
        self.path = os.path.realpath(path)
        self.loader = manager

    def retrieve(self, id):
        return self.loader.load(self.get_path(id))

    def exists(self, id):
        return os.path.isfile(self.get_path(id))

    def get_path(self, id):

        paths = [
            ("%s/%s" % (self.path, id), id),
            ("%s/%s.yml" % (self.path, id), id),
            ("%s/%s/_index.yml" % (self.path, id), id),
        ]

        for path, id in paths:
            if os.path.isfile(path):
                return path

    
    def save(self, id, type, data):        
        path = self.get_path(id)

        data['type'] = type

        print path, data

        self.loader.save(path, data)


    def find(self, type=None, types=None, tag=None, tags=None, category=None, path=None, offset=None, limit=None):
        """
        Of course this is not optimized at all

            supported options:
                - path: the path to look up
                - type: the node type
                - types: retrieve types defined
                - tags: retrieve node matching tags
                - category: retrieve node matching the category

        """
        options = options = {}

        lookup_path = self.path
        if path:
            lookup_path = "%s/%s" % (self.path, path)

        lookup_types = types or []
        if type:
            lookup_types.append(type)

        lookup_tags = tags or []
        if tag:
            lookup_tags.append(tag)

        nodes = []
        for (path, dirs, files) in os.walk(lookup_path):
            for file in files:
                filename = os.path.realpath("%s/%s" % (path, file))

                if filename[0:len(self.path)] != self.path:
                    # security issue, try to access path outside the self.path
                    continue

                if not self.loader.supports(filename):
                    continue

                node = self.loader.load(filename)

                if not node:
                    continue

                node['id'] = filename[(len(self.path)+1):] # no starting slash

                if node['id'][-4:] == '.yml':
                    node['id'] = node['id'][:-4]

                    if node['id'][-6:] == '_index':
                        node['id'] = node['id'][:-7]

                if 'type' not in node or (len(lookup_types) > 0 and node['type'] not in lookup_types):
                    continue

                if len(lookup_tags) > 0 and 'tags' not in node:
                    continue

                if 'tags' in node and len(lookup_tags) > 0:
                    skip = False
                    for tag in lookup_tags:
                        if tag not in node['tags']:
                            skip = True

                    if skip:
                        continue

                if category and 'category' not in node and category != node['category']:
                    continue

                nodes.append(node)

        return nodes[offset:limit]

    def find_one(self, options=None, selector=None, **kwargs):
        return find(**kwargs)[0]
