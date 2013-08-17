var elementModule = angular.module('element', ['nodeServices', 'ngCookies']);

elementModule.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/node/list', {templateUrl: 'partials/node-list.html', controller: NodeListCtrl})
        .when('/node/view/:id', {templateUrl: 'partials/node-detail.html', controller: NodeDetailCtrl})
        .when('/node/edit/:id', {templateUrl: 'partials/node-edit.html', controller: NodeEditCtrl})

        .otherwise({redirectTo: '/node/list'})
    ;
}]);

jQuery.ajax({
    url: '/api/element/handlers.json',
    type: 'GET',
    success: function(pager) {
        var handlers = []

        jQuery(pager.results).each(function(key, handler) {
            handlers.push("/api/element/handler/" + handler.code + ".js?ctx=admin");
        });

        
    }
});        
