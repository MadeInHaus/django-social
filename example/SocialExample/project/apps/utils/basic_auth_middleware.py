import base64
from django.http import HttpResponse
from django.middleware.common import CommonMiddleware
from django.conf import settings

class AuthMiddleware(CommonMiddleware):
    """
Add this to middleware:
'utils.basic_auth_middleware.AuthMiddleware',


Add these settings:
USE_BASIC_AUTH = True
BASIC_AUTH_USER = 'user'
BASIC_AUTH_PASS = 'password'

"""

    def process_request(self, request):
        if getattr(settings, 'USE_BASIC_AUTH', False):
            if request.META.get('HTTP_AUTHORIZATION', False):
                authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
                auth = base64.b64decode(auth)
                username, password = auth.split(':')
                if (username == getattr(settings, 'BASIC_AUTH_USER', None) 
                    and password == getattr(settings, 'BASIC_AUTH_PASS', None)):
                    return
            r = HttpResponse("Auth Required", status = 401)
            r['WWW-Authenticate'] = 'Basic realm="bat"'
            return r
