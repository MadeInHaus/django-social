from instagram.oauth2 import OAuth2API
from instagram.models import Media
from instagram.bind import bind_method

MEDIA_ACCEPT_PARAMETERS = ["count", "max_id"]

class InstagramAPI(OAuth2API):
    host = "api.instagram.com"
    base_path = "/v1"
    access_token_field = "access_token"
    authorize_url = "https://api.instagram.com/oauth/authorize"
    access_token_url = "https://api.instagram.com/oauth/access_token"
    protocol = "https"
    api_name = "Instagram"
    format = 'json'
    
    _tag_recent_media = bind_method(
            path="/tags/{tag_name}/media/recent",
            accepts_parameters=MEDIA_ACCEPT_PARAMETERS + ['tag_name'],
            root_class=Media,
            paginates=True,
            objectify_response=False)

    def tag_recent_media(self,tag,max_id):
        return self._tag_recent_media(tag_name=tag,max_id=max_id,count=100)[0]