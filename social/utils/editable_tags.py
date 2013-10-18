'''
Created on Oct 17, 2013

@author: joshua
'''
from django.utils.safestring import mark_safe


def editable_tags(field):
    def _f(self):
        s = """
<select multiple id="select{pk}" class="tag-select">
<option value="1" selected>Legal</option>
<option value="2">French</option>
<option value="3">English</option>
<option value="4">German</option>
<option value="5">Japanese</option>
<option value="6">Chinese</option>
<option value="7" selected>Porn</option>
</select>
        """.format(**{'pk': self.pk})
        s = mark_safe(s)
        s2 = "{}".format(' '.join(map(unicode, getattr(self, field.name).all())))
        return s
    _f.short_description = field.verbose_name
    _f.allow_tags = True
    return _f
