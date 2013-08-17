var nodeServices = angular.module('nodeServices', ['ngResource']);

nodeServices.factory('Node', function($resource) {
    return $resource('/api/element/node/:id.json', {}, {
        get:    {method: 'GET', params:{id: 'id'}},
        query:  {method: 'GET', isArray: false},
        save:   {method: 'PUT', params:{id: '@id'}}
    });
});