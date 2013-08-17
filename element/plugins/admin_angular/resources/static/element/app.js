var elementModule = angular.module('element', ['nodeServices', 'ngCookies']);

elementModule.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/node/list', {templateUrl: 'element/partials/node-list.html', controller: NodeListCtrl})
        .when('/node/view/:id', {templateUrl: 'element/partials/node-detail.html', controller: NodeDetailCtrl})
        .when('/node/edit/:id', {templateUrl: 'element/partials/node-edit.html', controller: NodeEditCtrl})

        .otherwise({redirectTo: '/node/list'})
    ;
}]);