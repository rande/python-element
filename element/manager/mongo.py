from bson.objectid import ObjectId, InvalidId
from bson.dbref import DBRef
import pymongo

class InvalidTreeState(Exception):
    pass

class InvalidDataFormat(Exception):
    pass

class MongoManager(object):
    """
    This class handle loading of definition from a MongoDB Server
    """
    def __init__(self, client, database, collection, logger=None):
        self.client = client
        self.database = database
        self.collection = collection
        self.logger = logger

        self.get_collection().ensure_index([("path", pymongo.ASCENDING)], 300, **{
            "name": "path",
            "unique": True,
            "background": False,
            "sparse": False,
        })

    def get_collection(self):
        return self.client[self.database][self.collection]

    def get_id(self, mid):
        if isinstance(mid, ObjectId):
            return mid

        try:
            return ObjectId(mid)
        except InvalidId, e:
            return None

    def retrieve(self, mid):
        data = self.get_collection().find_one({"_id": self.get_id(mid)})

        if not data:
            return None

        return self.normalize([data])[0]

    def exists(self, mid):
        return self.get_collection().find({"_id": self.get_id(mid)}).count() > 0

    def delete(self, mid):
        result = self.get_collection().remove(self.get_id(mid), j=True)

        return result[u'n']

    def resolve_parents(self, data):
        if 'parent' not in data:
            data['parent'] = None

    def fix_paths(self, data):
        path = False

        if not data['parent']:  # no parent
            path = ""

        if 'slug' not in data:  # no parent
            raise InvalidDataFormat("No slug property defined for the data")

        if data['parent']:
            parent = self.retrieve(data['parent'])

            if not parent:
                raise InvalidTreeState("The parent %s defined in %s does not exist" % (data['id'], data['parent']))

            if 'path' not in parent:
                raise InvalidTreeState("The parent %s does not contains a `path`" % (parent['id']))

            path = parent['path']

        if path == False:
            raise InvalidTreeState("Unable to resolve the path for %s" % (data))

        data['path'] = "%s/%s" % (path, data['slug'])

    def fix_children(self, data):
        children = self.get_collection().find({
            'parent': "%s" % data['_id']
        })

        for child in children:
            path = "%s/%s" % (data['path'], child['slug'])

            if child['path'] == path:
                continue

            child['path'] = path

            self.get_collection().save(child)
            self.fix_children(child)

    def save(self, mid, data):
        """
        Save data and resolve the path for the children
        """

        if 'slug' not in data:
            raise InvalidDataFormat("The data must contain a `slug` key: %s" % (data))

        if mid:
            data['_id'] = ObjectId(mid)

        self.resolve_parents(data)
        self.fix_paths(data)

        data['_id'] = self.get_collection().save(data)

        self.fix_children(data)
        self.normalize([data])

        return data

    def find(self, **kwargs):
        """
        Of course this is not optimized at all

            supported options:
                - path: the path to look up
                - type: the node type
                - types: retrieve types defined
                - tags: retrieve node matching tags
                - category: retrieve node matching the category

        """
        find_kwargs = {
            'spec': {}
        }

        lookup_types = []
        if 'types' in kwargs:
            lookup_types += kwargs['types']

        if 'type' in kwargs:
            lookup_types += [kwargs['type']]

        if len(lookup_types) > 0:
            find_kwargs['spec']['type'] = {'$in': lookup_types}

        if 'tags' in kwargs and kwargs['tags'] and len(kwargs['tags']) > 0:
            find_kwargs['spec']['tags'] = {'$in': kwargs['tags']}

        if 'category' in kwargs and kwargs['category'] != None:
            find_kwargs['spec']['category'] = kwargs['category']

        if 'limit' in kwargs:
            find_kwargs['limit'] = int(kwargs['limit'])

        if 'offset' in kwargs:
            find_kwargs['omit'] = int(kwargs['offset'])

        if 'alias' in kwargs and kwargs['alias']:
            find_kwargs['spec']['path'] = kwargs['alias']

        if 'path' in kwargs and kwargs['path']:
            find_kwargs['spec']['path'] = {'$regex': "^" + kwargs['path']}

        if self.logger:
            self.logger.info("element.manager.mongo: find:%s" % (find_kwargs))

        query = self.get_collection().find(**find_kwargs)

        if 'order_by' in kwargs:
            query.sort(kwargs['order_by'])
        else:
            query.sort([('created_at', pymongo.DESCENDING)])

        return self.normalize(query)

    def find_one(self, **kwargs):
        return self.find(**kwargs)[0]

    def normalize(self, cursor):
        """
        Far from being perfect
        """
        nodes = []
        for data in cursor:
            data['id'] = "%s" % data['_id']

            del data['_id']

            nodes.append(data)

        return nodes
