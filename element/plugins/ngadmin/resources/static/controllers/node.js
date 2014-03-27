function MainController($scope) {
    $scope.$on('element.node.load', function(event, args) {
        console.log('element.node.load', args);
    });

    $scope.$on('element.node.save', function(event, args) {
        console.log('element.node.save', args);
    });
}

function NodeListCtrl($scope, Node) {
    $scope.nodes = Node.query();
}

function NodeDetailCtrl($scope, $routeParams, $http, Node) {
    $scope.node = Node.get({uuid: $routeParams.uuid});
}

function NodeEditCtrl($scope, $routeParams, $http, Node) {
    function load_node(uuid) {
        $scope.node = Node.get({uuid: uuid}, function(node) {
            node.category = !node.category ? '' : node.category;
            node.tags = node.tags.join(", ");

            $scope.$emit('element.node.load', {'node': node});

            // add an event to normalize the loaded node
        });
    }

    load_node($routeParams.uuid);
    
    $scope.get_template = function(node) {
        return "/element/static/element.plugins.ngadmin/partials/node/" + node.type + ".edit.html";
    };

    $scope.save = function() {

        $scope.$emit('element.node.save', {'node': $scope.node});

        // fix denormalize value
        if ($scope.node.category == '') {
            $scope.node.category = false
        }

        $scope.node.uuid = jQuery.trim($scope.node.uuid)

        $scope.node.tags = jQuery.map($scope.node.tags.split(","), function(data) {
            return jQuery.trim(data);
        });

        $scope.node.$save(function(node) {
            load_node($scope.node.uuid)
        })
    }
}