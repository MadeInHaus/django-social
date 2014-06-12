from django.conf.urls import patterns

from social.views import thanks, instauth
from django.conf.urls import url

from utils.editable_tags import EditableTagsView

urlpatterns = patterns('',
    url(r'thanks/', thanks, name="twitter_callback"),
    url(r'instauth/', instauth, name="instagram_callback"),
    url(r'editable-tags/select-(?P<pk>\w+)/', EditableTagsView.as_view()),
)
