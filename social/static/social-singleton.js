function f() {
	var $ = django.jQuery;
	if ($('div[data-singleton=true]').length) {
		$('input[name=_addanother]').parent().hide();
	}
};

django.jQuery(document).ready(f)
