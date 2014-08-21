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

from element.manager import generate_uuid, InvalidDataFormat, InvalidTreeState
from elasticsearch import Elasticsearch

class ElasticSearchManager(object):
    """
    This class handle loading of definition from a MongoDB Server
    """
    def __init__(self, index='element', logger=None):
        self.client = Elasticsearch()
        self.index = index
        self.logger = logger

        mappings = dict()
        # need to iterate over node types available to alter the definition
        mappings["node"] = {
            "_source": {"enabled": True},
            "properties": {
                "uuid":   {"type": "string", "index": "not_analyzed"},
                "parent": {"type": "string", "index": "not_analyzed"},
                "type":   {"type": "string", "index": "not_analyzed"},
                "tags":   {"type": "string", "index": "not_analyzed",  "index_name": "tag"}
            }
        }

        self.client.indices.create(index=self.index, ignore=400, body={
            "mappings": mappings
        })

    def get_id(self, id):
        return id

    def retrieve(self, uuid):
        res = self.client.search(index=self.index, body={
            "query": {
                "term": {
                    "uuid": uuid
                }
            },
            "size": 10
        })

        # print "UUID", uuid, res
        results = self.normalize(res)

        if len(results) > 0:
            return results[0]

        return None

    def exists(self, uuid):
        return self.client.count(index=self.index, body={
            "query": {
                "term": {
                    "uuid": uuid
                }
            },
            "size": 1
        })['count'] > 0

    def delete(self, uuid):
        result = self.client.delete_by_query(index=self.index, body={
            "query": {
                "term": {
                    "uuid": uuid
                }
            },
            "size": 1
        })

        return True

    def resolve_parents(self, data):
        if 'parent' not in data:
            data['parent'] = None

    def fix_children(self, data):
        children = self.find(**{
            'parent': data['uuid']
        })

        for child in children:
            path = "%s/%s" % (data['path'], child['slug'])

            if child['path'] == path:
                continue

            child['path'] = path

            self.client.update(index=self.index, id=child['id'], refresh=True, doc_type="node", body={
                'doc': {'path': path}
            })

            self.fix_children(child)

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


    def save(self, uuid, data):
        """
        Save data and resolve the path for the children
        """
        if 'slug' not in data:
            raise InvalidDataFormat("The data must contain a `slug` key: %s" % (data))

        if not uuid:
            uuid = generate_uuid()

        data['uuid'] = uuid

        kwargs = {
            'index': self.index,
            'doc_type': 'node',
            'body': data,
            # refresh=True, this is not ideal but required to have real time data inside the index
            'refresh': True
        }

        if 'id' in data:
            kwargs['id'] = data['id']
            del(data['id'])

        self.resolve_parents(data)
        self.fix_paths(data)


        res = self.client.index(**kwargs)

        data['id'] = res['_id']

        self.fix_children(data)
        # self.normalize([data])

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
            'index': self.index,
            'body': {
                'size': 25,
                'from': 0,
                'query': {
                    'filtered': {
                        'query':  {},
                        'filter': {}
                    }
                }
            }
        }

        query = {
            "bool": {
                "must": []
            }
        }

        lookup_types = []
        if 'types' in kwargs:
            lookup_types += kwargs['types']

        if 'type' in kwargs:
            lookup_types += [kwargs['type']]

        for type in lookup_types:
            query['bool']['must'].append({'match': {'type': type}})

        if 'tags' in kwargs and kwargs['tags'] and len(kwargs['tags']) > 0:
            for tag in kwargs['tags']:
                query['bool']['must'].append({'match': {'tag': tag}})

        if 'category' in kwargs and kwargs['category'] != None:
            query['bool']['must'].append({'match': {'category': kwargs['category']}})

        if 'parent' in kwargs and kwargs['parent'] != None:
            query['bool']['must'].append({'match': {'parent': kwargs['parent']}})

        if 'limit' in kwargs:
            find_kwargs['body']['limit'] = int(kwargs['limit'])

        if 'offset' in kwargs:
            find_kwargs['body']['from'] = int(kwargs['offset']) * find_kwargs['body']['limit']

        # if 'alias' in kwargs and kwargs['alias']:
        #     find_kwargs['spec']['path'] = kwargs['alias']
        #
        # if 'path' in kwargs and kwargs['path']:
        #     find_kwargs['spec']['path'] = {'$regex': "^" + kwargs['path']}
        #
        # if self.logger:
        #     self.logger.info("element.manager.mongo: find:%s" % (find_kwargs))
        #

        #
        # if 'order_by' in kwargs:
        #     query.sort(kwargs['order_by'])
        # else:
        #     query.sort([('created_at', pymongo.DESCENDING)])

        if len(query['bool']['must']) == 0:
            # we need to match all documents otherwise with have an exception
            find_kwargs['body']['query']['filtered']['query'] = {"bool": {"should": [{"match_all": {}}]}}
        else:
            find_kwargs['body']['query']['filtered']['query'] = query

        res = self.client.search(**find_kwargs)

        return self.normalize(res)

    def find_one(self, **kwargs):
        return self.find(**kwargs)[0]

    def normalize(self, cursor):
        """
        Far from being perfect
        """
        nodes = []
        for data in cursor['hits']['hits']:
            data['_source'].update({'id': data['_id']})

            nodes.append(data['_source'])

        return nodes
