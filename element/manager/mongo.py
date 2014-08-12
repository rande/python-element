#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from bson.objectid import ObjectId, InvalidId
import pymongo
from element.manager import generate_uuid

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

        self.get_collection().ensure_index([("type", pymongo.ASCENDING)], 300, **{
            "name": "type",
            "unique": False,
            "background": False,
            "sparse": False,
        })

        self.get_collection().ensure_index([("uuid", pymongo.ASCENDING)], 300, **{
            "name": "uuid",
            "unique": True,
            "background": False,
            "sparse": False,
        })

        self.get_collection().ensure_index([("alias", pymongo.ASCENDING)], 300, **{
            "name": "uuid",
            "unique": False,
            "background": False,
            "sparse": False,
        })

        self.get_collection().ensure_index([
            ("type", pymongo.ASCENDING),
            ("tag", pymongo.ASCENDING),
            ("path", pymongo.ASCENDING),
        ], 300, **{
            "name": "type",
            "unique": False,
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

    def retrieve(self, uuid):
        data = self.get_collection().find_one({"uuid": uuid})

        if not data:
            return None

        return self.normalize([data])[0]

    def exists(self, uuid):
        return self.get_collection().find({"uuid": uuid}).count() > 0

    def delete(self, uuid):
        result = self.get_collection().remove({"uuid": uuid}, j=True)

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
                raise InvalidTreeState("The parent %s defined in %s does not exist" % (data['uuid'], data['parent']))

            if 'path' not in parent:
                raise InvalidTreeState("The parent %s does not contains a `path`" % (parent['uuid']))

            path = parent['path']

        if path == False:
            raise InvalidTreeState("Unable to resolve the path for %s" % (data))

        data['path'] = "%s/%s" % (path, data['slug'])

    def fix_children(self, data):
        children = self.get_collection().find({
            'parent': "%s" % data['uuid']
        })

        for child in children:
            path = "%s/%s" % (data['path'], child['slug'])

            if child['path'] == path:
                continue

            child['path'] = path

            self.get_collection().save(child)
            self.fix_children(child)

    def save(self, uuid, data):
        """
        Save data and resolve the path for the children
        """

        if 'slug' not in data:
            raise InvalidDataFormat("The data must contain a `slug` key: %s" % (data))

        if not uuid:
            uuid = generate_uuid()

        if 'id' in data:
            data['_id'] = ObjectId(data['id'])
            del(data['id'])

        data['uuid'] = uuid

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
