requirejs.config({
    //By default load any module IDs from js/lib
    baseUrl: '/element/static/admin/',

    urlArgs: "bust=" +  (new Date()).getTime()

    //except, if the module ID starts with "app",
    //load it from the js/app directory. paths
    //config is relative to the baseUrl, and
    //never includes a ".js" extension since
    //the paths config could be for a directory.
    // paths: {
        // app: '../app'
    // }
});

// Start the main app logic.
requirejs([
	'jquery/jquery', 
	'bootstrap/js/bootstrap.min', 
	'angular/angular',
	'angular/angular-resource',
	'angular/angular-cookies',
	'element/services/data-mapper',
	'element/services/node-handler',
	'element/controllers/node',
	'element/app'
],
function($) {
    //jQuery, canvas and the app/sub module are all
    //loaded and can be used here now.

    
    jQuery.ajax({
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
});