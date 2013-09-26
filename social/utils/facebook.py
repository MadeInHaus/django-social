'''
Created on Sep 26, 2013
'''

from urlparse import parse_qs, urlparse

def parse_facebook_picture_embed(msg, width="200px", height="200px"):
    """ returns facebook picture embed link """
    # instagram videos and other types of facebook vids could also be parsed here
    picture = msg.get('picture', '')
    if picture is not None and 'safe_image.php' in picture:
        picture = parse_qs(urlparse(picture).query).get('url', [None,])[0]
    picture = picture.replace('_s', '_b').replace('_t', '_b')

    if not picture:
        return "no media found"
    return '<img src="{}" width="{}" height="{}">'.format(picture, width, height)

    return picture

def parse_facebook_video_embed(msg, width="200px", height="200px"):
    """ returns html for embedding video, returns a picture if video not embeddable """
    link = msg.get('link') or msg.get('source') or None
    if link:
        params = parse_qs(urlparse(link).query)
        vid = params.get('v',[''])[0]
        if 'youtube' in link:
            return '<iframe src="//www.youtube.com/embed/{}" width="{}" height="{}" frameborder="0" allowfullscreen></iframe>'.format(vid, width, height)
        elif 'facebook' in link:
            return '<iframe src="https://www.facebook.com/video/embed?video_id={}" width="{}" height="{}" frameborder="0"></iframe>'.format(vid, width, height)
        else:
            return parse_facebook_picture_embed(msg)
