requirejs.config({
    baseUrl: '/element/static/'
    ,urlArgs: "bust=" +  (new Date()).getTime()
});

// Start the main app logic.
requirejs([
	'element.plugins.jquery/jquery', 
	'element.plugins.bootstrap/js/bootstrap.min', 
	'element.plugins.angular/angular',
	'element.plugins.angular/angular-resource',
	'element.plugins.angular/angular-cookies',
],
function($) {
    
    requirejs([
        'element.plugins.admin/services/data-mapper',
        'element.plugins.admin/services/node-handler',
        'element.plugins.admin/controllers/node',
        'element.plugins.admin/app'
    ],
    function($) {
        jQuery.ajax({
            
            // angular.bootstrap("element");

            url: '/api/element/handlers.json',
            type: 'GET',
            success: function(pager) {
                var handlers = []

                jQuery(pager.results).each(function(key, handler) {
                    handlers.push("/api/element/handler/" + handler.code + ".js?ctx=admin");
                });

                requirejs(handlers);
            }
        });        
    })
});