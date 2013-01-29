/*
	the projects require.js config,
	used in build process also
	see: http://requirejs.org/docs/api.html#config
*/

/*global requirejs*/
requirejs.config({
	//tell require.js what global this lib makes
	shim: {
		'underscore': { exports: '_' },
		'backbone': { deps: ['underscore','jquery'], exports: 'Backbone' },
		'modernizr': { exports: 'Modernizr' }
	},
	//re-route libs to top-level
	paths: {
		'jquery': 'libs/jquery',
		'backbone': 'libs/backbone',
		'underscore': 'libs/underscore',
		'text': 'libs/text',
		'domReady': 'libs/domReady',
		'modernizr': 'libs/modernizr'
	}
});