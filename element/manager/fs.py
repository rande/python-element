import os
from element.exceptions import SecurityAccessException

class FsManager(object):
    """
    This class handle loading of definition from the Filesystem
    """
    def __init__(self, path, loader, logger=None):
        self.path = os.path.realpath(path)
        self.loader = loader
        self.logger = None

    def retrieve(self, id):
        return self.loader.load(self.get_path(id))

    def exists(self, id):
        path = self.get_path(id)

        if not path:
            return False

        return os.path.isfile(path)

    def get_path(self, id):
        paths = [
            ("%s/%s" % (self.path, id), id),
            ("%s/%s.yml" % (self.path, id), id),
            ("%s/%s/_index.yml" % (self.path, id), id),
        ]

        for path, id in paths:
            if os.path.isfile(path):
                path = os.path.realpath(path)
                break

        if not path.startswith(self.path):
            raise SecurityAccessException(path)

        return path

    def get_new_path(self, id):
        # the file exists, return the path
        path = "%s/%s" % (self.path, id)
        if os.path.isfile(path):
            return path

        # check if the extension is not yml ...
        basename, extension = os.path.splitext(path)        
        if extension != 'yml' and len(extension.strip()) > 0:
            return path

        # check is the yml def exist
        path = "%s/%s.yml" % (self.path, id)
        if os.path.isfile(path):
            return path

        # ok, check is a path exist, if so we try to save an index
        path = "%s/%s" % (self.path, id)
        if os.path.isdir(path):
            return "%s/_index.yml" % path

        # the path does not exist create it ...
        return "%s/%s.yml" % (self.path, id)

    def delete(self, id):
        if not self.exists(id):
            return False

        os.remove(self.get_path(id))

        return True

    def save(self, id, type, data):        
        path = self.get_new_path(id)

        data['type'] = type

        basepath, filename = os.path.split(path)
        basename, extension = os.path.splitext(filename)

        if not os.path.isdir(basepath):
            os.makedirs(basepath)

        return self.loader.save(path, data)

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
        lookup_path = self.path
        if path:
            lookup_path = "%s/%s" % (self.path, path)

        lookup_types = types or []
        if type:
            lookup_types.append(type)

        lookup_tags = tags or []
        if tag:
            lookup_tags.append(tag)

        if self.logger:
            self.logger.info("%s find:%s" % (self, {
                'type': type, 'types': types, 'tag': tag, 'tags': tags,
                'path': path, 'offset': offset, 'limit': limit
            }))

        nodes = []
        for (path, dirs, files) in os.walk(lookup_path):
            for file in files:
                filename = os.path.realpath("%s/%s" % (path, file))

                if not filename.startswith(self.path):
                    raise SecurityAccessException(filename)

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

        results = self.find(**kwargs)

        if len(results) > 0:
            return results[0]

        return None
