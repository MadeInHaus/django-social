import json
from django.http import HttpResponseRedirect, HttpResponseServerError,\
    HttpResponse
    
import sys
import traceback

import calendar, datetime


def JSON_response(response_dict, success=None, error=None, browser_caching=False, request=None):
    callback = request.GET.get('callback', None) if request is not None else None

    # Renders an HttpResponse with JSON body corresponding to response_dict
    response = None
    try:
        response_str = json.dumps(response_dict, default=encode)
        if callback:
            if response_str[0] not in ['"', '[', '{'] \
                    or response_str[-1] not in ['"', ']', '}']:
                response_str = '"%s"' % response_str
            response_str = "%s(%s)" % (callback, response_str)

        try:
            if response_dict.has_key('error'):
                if error:
                    return HttpResponseRedirect(error)
                response = HttpResponseServerError(response_str, mimetype="application/json")
        except:
            pass # response may not be a dict
        
        if success:
            return HttpResponseRedirect(success)

        response = HttpResponse(response_str, mimetype="application/json")
    except:
        print >> sys.stderr, "Problem Rendering JSON:"
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        if error:
            return HttpResponseRedirect(error)
        response = HttpResponseServerError('{"error": "problem rendering JSON response"}', mimetype="application/json")

    if response is None:
        response = HttpResponseServerError('{"error": "problem rendering JSON response:  RESPONSE was None"}', mimetype="application/json")

    if not browser_caching:
        response['Expires'] = -1
        response['CacheControl'] = 'no-cache'

    if callback:
        response['Content-Type'] = 'application/javascript'

    return response


def HTML_response(d, browser_caching=False):
    s = """<html><head><title>Break</title></head><body><div>%s</div></body></html> """ % str(d)
    response = HttpResponse(s)

    if not browser_caching:
        response['Expires'] = -1
        response['CacheControl'] = 'no-cache'

    return response


def encode(obj):
    
    if isinstance(obj, datetime.datetime):
        return calendar.timegm(obj.timetuple())*1000
    
    raise TypeError("%r type %s is not JSON serializable, dude" % (obj, type(obj)))
