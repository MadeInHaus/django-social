(function($, undefined) {
	var updateTags = function(event, ui) {
		var id = $(this).attr('id');
		var tags = $(this).val();
		
		d = {'id': id, 'tags': tags}
		
        console.log("select:", $(this).val(), ui, d);
        $.ajax({
            type: "POST",
            url: "/social/editable-tags/"+id+"/",
            data:  JSON.stringify(d),
            contentType: 'application/json; charset=utf-8',
            dataType: 'text',
            success: function(data) {
           	 console.log("data: ", data);
            },
            error: function() {
           	 
            },
        });
	};
	
	console.log("XXXX");
	$(document).ready(function() {$(".tag-select").multiselect({
	    selectedText: "# of # selected",
	    selectedList: 40,
	    close: updateTags
	});});

	
}) (django.jQuery)