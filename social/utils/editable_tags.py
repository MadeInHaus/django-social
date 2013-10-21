'''
Created on Oct 17, 2013

@author: joshua
'''
from django.utils.safestring import mark_safe
from django.views.generic.base import View

from taggit.models import Tag

from .json_response import JSON_response

from logging import getLogger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseForbidden
from json import loads
from django.shortcuts import get_object_or_404
log = getLogger(__name__)

def editable_tags(field):
    def _f(self):
        tags = Tag.objects.all()
        my_tags = getattr(self, field.name).all()
        
        s = """<div class="tag-select-wrapper"><select multiple id="select-{pk}" class="tag-select">""".format(**{'pk': self.pk})

        for tag in tags:
            s += "<option value={} {}>{}</option>".format(tag.slug, 'selected' if tag in my_tags else '', tag.name)

        s += """</select></div>"""

        s = mark_safe(s)
        return s

    _f.short_description = field.verbose_name
    _f.allow_tags = True
    return _f


class EditableTagsView(View):
    def post(self, request, pk=None):
        if not request.user or not request.user.is_active or not request.user.is_staff:
            return HttpResponseForbidden()

        from ..models import Message
        msg = get_object_or_404(Message, pk=pk)
        data = loads(request.body)
        tags = data.get('tags', None)
        if tags:
            msg._tags.set(*tags)
        else:
            msg._tags.clear()
        
        d = {"pk": pk, "msg.tags": map(unicode, msg._tags.names())}
        
        return JSON_response(d)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(EditableTagsView, self).dispatch(*args, **kwargs)