class ChainManager(object):
    """
    This class handle loading of definition from a MongoDB Server
    """
    def __init__(self, managers, logger=None):
        self.managers = managers or []
        self.logger = logger

    def retrieve(self, uuid):
        if self.logger:
            self.logger.debug("element.manager.chain: retrieve uuid:%s" % uuid)

        for name, manager in self.managers:
            data = manager.retrieve(uuid)

            if data:
                data['manager'] = name
                return data

        raise Exception("unable to retrieve the data with uuid: %s" % uuid)

    def exists(self, uuid):
        for name, manager in self.managers:
            if manager.exists(uuid):
                return True

        return False

    def delete(self, uuid):
        for name, manager in self.managers:
            deleted = manager.delete(uuid)
            
            if deleted:
                return True

        return False

    def save(self, uuid, data):
        if 'manager' not in data:
            raise Exception('no manager defined, cannot save data with reference: %s' % data)

        for name, manager in self.managers:
            if data['manager'] == name:
                return manager.save(uuid, data)

        return False

    def find(self, **kwargs):
        """
        Of course this is not optimized at all

            supported options:
                - path: the path to look up
                - type: the node type
                - types: retrieve types defined
                - tags: retrieve node matching tags
                - category: retrieve node matching the category
                - manager: find only nodes on the provided manager

        """
        datas = []

        if self.logger:
            self.logger.debug("element.manager.chain: find %s" % kwargs)

        for name, manager in self.managers:

            if "manager" in kwargs and name != kwargs["manager"]:
                continue

            elements = manager.find(**kwargs)

            for element in elements:
                element['manager'] = name

                datas.append(element)

        limit = None
        offset = 0

        if 'offset' in kwargs:
            offset = kwargs['offset']

        if 'limit' in kwargs:
            limit = kwargs['limit'] + offset

        # this is a bug as this can cut valid results from one manager
        return datas[offset:limit]

    def find_one(self, **kwargs):
        results = self.find(limit=1, **kwargs)

        if results:
            return results[0]

        return None