var nodeServices = angular.module('nodeServices', ['ngResource']);

nodeServices.factory('Node', function($resource) {
    return $resource('/api/element/node/:uuid.json', {}, {
        get:    {method: 'GET', params:{uuid: 'uuid'}},
        query:  {method: 'GET', isArray: false},
        save:   {method: 'PUT', params:{uuid: '@uuid'}}
    });
});