import os
from element.exceptions import SecurityAccessException
from element.manager import is_uuid, get_uuid

class FsManager(object):
    """
    This class handle loading of definition from the Filesystem
    """
    def __init__(self, path, loader, logger=None):
        self.path = os.path.realpath(path)
        self.loader = loader
        self.logger = None
        self.files  = {}
        self.ignore_files = [
            '.DS_Store'
        ]

    def retrieve(self, fid):
        if is_uuid(fid):
            fid = self.files[fid]

        node = self.loader.load(self.get_path(fid))

        node['id'] = fid
        node['uuid'] = get_uuid(node['id'])

        return node

    def exists(self, fid):
        if is_uuid(fid):
            fid = self.files[fid]

        path = self.get_path(fid)

        if not path:
            return False

        return os.path.isfile(path)

    def add_reference(self, path):
        fid = self.get_id_from_path(path)

        self.files[get_uuid(fid)] = fid

    def build_references(self):
        """
        This function build an array with all
        """
        for (path, dirs, files) in os.walk(self.path):
            for file in files:
                if file in self.ignore_files:
                    continue

                self.add_reference("%s/%s" % (path, file))

    def get_path(self, fid):
        paths = [
            ("%s/%s" % (self.path, fid), fid),
            ("%s/%s.yml" % (self.path, fid), fid),
            ("%s/%s/_index.yml" % (self.path, fid), fid),
        ]

        path = False

        for path, _ in paths:
            if os.path.isfile(path):
                path = os.path.realpath(path)
                break

        if not path.startswith(self.path):
            raise SecurityAccessException(path)

        return path

    def get_new_path(self, fid):
        # the file exists, return the path
        path = "%s/%s" % (self.path, fid)
        if os.path.isfile(path):
            return path

        # check if the extension is not yml ...
        basename, extension = os.path.splitext(path)        
        if extension != 'yml' and len(extension.strip()) > 0:
            return path

        # check is the yml def exist
        path = "%s/%s.yml" % (self.path, fid)
        if os.path.isfile(path):
            return path

        # ok, check is a path exist, if so we try to save an index
        path = "%s/%s" % (self.path, fid)
        if os.path.isdir(path):
            return "%s/_index.yml" % path

        # the path does not exist create it ...
        return "%s/%s.yml" % (self.path, fid)

    def delete(self, fid):
        if not self.exists(fid):
            return False

        os.remove(self.get_path(fid))

        return True

    def save(self, fid, data):
        path = self.get_new_path(fid)

        basepath, filename = os.path.split(path)
        basename, extension = os.path.splitext(filename)

        if not os.path.isdir(basepath):
            os.makedirs(basepath)

        return self.loader.save(path, data)

    def get_id_from_path(self, path):
        fid = path[(len(self.path)+1):]  # no starting slash

        if fid[-4:] == '.yml':
            fid = fid[:-4]

            if fid[-6:] == '_index':
                fid = fid[:-7]

        return fid

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

                node['id'] = self.get_id_from_path(filename)
                node['uuid'] = get_uuid(node['id'])

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
