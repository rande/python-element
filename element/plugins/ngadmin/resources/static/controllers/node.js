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
    $scope.node = Node.get({id: $routeParams.id});
}

function NodeEditCtrl($scope, $routeParams, $http, Node) {
    function load_node(id) {
        $scope.node = Node.get({id: id}, function(node) {
            node.data.category = !node.data.category ? '' : node.data.category;
            node.data.tags = node.data.tags.join(", ");

            $scope.$emit('element.node.load', {'node': node});

            // add an event to normalize the loaded node
        });
    }

    load_node($routeParams.id);
    
    $scope.get_template = function(node) {
        return "/element/static/element.plugins.ngadmin/partials/node/" + node.type + ".edit.html";
    };

    $scope.save = function() {

        $scope.$emit('element.node.save', {'node': $scope.node});

        // fix denormalize value
        if ($scope.node.data.category == '') {
            $scope.node.data.category = false
        }

        $scope.node.id = jQuery.trim($scope.node.id)

        $scope.node.data.tags = jQuery.map($scope.node.data.tags.split(","), function(data) {
            return jQuery.trim(data);
        });

        $scope.node.$save(function(node) {
            load_node($scope.node.id)
        })
    }
}