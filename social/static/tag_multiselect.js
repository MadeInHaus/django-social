(function($, undefined) {
	console.log("XXXX");
	$(document).ready(function() {$(".tag-select").multiselect({
	    selectedText: "# of # selected",
	    selectedList: 40,
	    click: function(event, ui) {
	         console.log("select:", $(this).val(), ui);   
	    }
	});});

	
}) (django.jQuery)