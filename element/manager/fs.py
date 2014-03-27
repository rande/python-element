import os
from element.exceptions import SecurityAccessException, InvalidDataException
from element.manager import is_uuid, get_uuid

class FsManager(object):
    """
    This class handle loading of definition from the Filesystem
    """
    def __init__(self, path, loader, logger=None):
        self.path = os.path.realpath(path)
        self.loader = loader
        self.logger = logger
        self.files  = {}
        self.ignore_files = [
            '.DS_Store'
        ]
        self.build_references()

    def get_fid(self, uuid):
        if not uuid:
            return None

        if not is_uuid(uuid):
            return None

        if uuid not in self.files:
            return None

        return self.files[uuid]

    def retrieve(self, uuid):
        fid = self.get_fid(uuid)

        node = self.loader.load(self.get_path(fid))

        if not node:
            return None

        node['id'] = fid
        node['uuid'] = uuid
        node['path'] = fid

        return node

    def exists(self, uuid):
        fid = self.get_fid(uuid)

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
        self.files = {}
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

    def delete(self, uuid):
        if not self.exists(uuid):
            return False

        fid = self.get_fid(uuid)

        os.remove(self.get_path(fid))

        return True

    def save(self, uuid, data):
        fid = self.get_fid(uuid)

        if not fid and 'path' not in data:
            raise InvalidDataException("Cannot save a not existent file with no path")

        if not fid:
            fid = data['path']

        path = self.get_new_path(fid)

        basepath, filename = os.path.split(path)
        basename, extension = os.path.splitext(filename)

        if not os.path.isdir(basepath):
            os.makedirs(basepath)

        self.add_reference(path)

        return self.loader.save(path, data)

    def get_id_from_path(self, path):

        fid = path[(len(self.path)+1):]  # no starting slash

        if fid[-4:] == '.yml':
            fid = fid[:-4]

            if fid[-6:] == '_index':
                fid = fid[:-7]

        return fid

    def load_node(self, filename):
        filename = os.path.realpath(filename)

        if not filename.startswith(self.path):
            raise SecurityAccessException(filename)

        if not self.loader.supports(filename):
            return None

        node = self.loader.load(filename)

        if not node:
            return None

        node['id'] = self.get_id_from_path(filename)
        node['uuid'] = get_uuid(node['id'])
        node['path'] = node['id']

        return node

    def find(self, type=None, types=None, tag=None, tags=None, category=None, alias=None, path=None, offset=None, limit=None):
        """
        Of course this is not optimized at all

            supported options:
                - path: the path to look up
                - type: the node type
                - types: retrieve types defined
                - tags: retrieve node matching tags
                - category: retrieve node matching the category

        """
        if self.logger:
            self.logger.info("element.manager.fs: find:%s" % ({
                'type': type, 'types': types, 'tag': tag, 'tags': tags,
                'alias': alias, 'path': path, 'offset': offset, 'limit': limit
            }))

        lookup_path = self.path
        if alias:
            fpath = self.get_path(alias)

            if fpath:
                node = self.load_node(fpath)

                if node:
                    return [node]
                else:
                    return []

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
                node = self.load_node("%s/%s" % (path, file))

                if not node:
                    continue

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
