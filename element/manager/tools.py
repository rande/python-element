class ChainManager(object):
    """
    This class handle loading of definition from a MongoDB Server
    """
    def __init__(self, managers):
        self.managers = managers or []

    def retrieve(self, reference):
        for name, manager in self.managers:
            try:
                data = manager.retrieve(reference)
                data['manager'] = name

                if data:
                    return data

            except Exception, e:
                # silently fail error
                pass
        
        raise Exception("unable to retrieve the data with reference: %s" % reference)

    def exists(self, reference):
        for name, manager in self.managers:
            if manager.exists(reference):
                return True

        return False

    def delete(self, reference):
        for name, manager in self.managers:
            deleted = manager.delete(reference)
            
            if deleted:
                return True

        return False

    def save(self, reference, type, data):
        if 'manager' not in data:
            raise Exception('no manager defined, cannot save data with reference: %s' % data)

        for name, manager in self.managers:
            if data['manager'] == name:
                return manager.save(reference, type, data)

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

        """
        datas = []

        for name, manager in self.managers:
            elements = manager.find(**kwargs)

            for element in elements:
                element['manager'] = name

                datas.append(element)

        limit = None
        offset = None

        if 'limit' in kwargs:
            limit = kwargs['limit']

        if 'offset' in kwargs:
            offset = kwargs['offset']

        # this is a bug as this can cut valid results from one manager
        return datas[offset:limit]

    def find_one(self, **kwargs):
        return self.find(limit=1, **kwargs)[0]